from copy import deepcopy
from sys import maxsize
from heapq import *
from riskGame.classes.state.move import Move


class State:

    def __init__(self, number_nodes, partitions, players, player_turn_number):
        self.__number_nodes = number_nodes
        self.__partitions = partitions
        self.__players = players
        self.__player_turn_number = player_turn_number
        self.__curr_bonus_node = None

    @property
    def set_bonus_node(self, node):
        self.__curr_bonus_node = node

    @property
    def get_bonus_node(self):
        return self.__curr_bonus_node

    @property
    def set_players(self, players):
        self.__players = players

    @property
    def set_number_nodes(self, number_nodes):
        self.__number_nodes = number_nodes

    @property
    def set_partitions(self, partitions):
        self.__partitions = partitions

    @property
    def set_player_turn_number(self, player_turn_number):
        self.__player_turn_number = player_turn_number

    @property
    def get_players(self):
        return self.__players

    @property
    def get_number_nodes(self):
        return self.__number_nodes

    @property
    def get_partitions(self):
        return self.__partitions

    @property
    def get_player_turn_number(self):
        return self.__player_turn_number

    def get_current_player(self):
        return self.__players[self.__player_turn_number]

    def get_next_player(self):
        return self.__players[(self.__player_turn_number + 1) % len(self.__players)]

    def get_winner(self):
        for player in self.__players:
            if len(player.get_hold_nodes()) == self.__number_nodes:
                return player
        return None

    def expand_bonus(self, limit=maxsize):
        curr_player = self.get_current_player()

        #get bonus
        curr_bonus = curr_player.get_bonus()

        #get border nodes
        border_nodes = curr_player.get_border_nodes()

        ret_states = []

        case1 = None
        case2 = None
        case1_diff = maxsize
        case2_diff = -maxsize

        for node in border_nodes:

            if node.can_attack():
                # already has more troops
                min_loss = node.min_loss_attack()
                if min_loss < case1_diff:
                    case1_diff = min_loss
                    case1 = node
            else:
                # TODO not use move_bonus unless you really move the bonus not just try to move bonus
                # as move_bonus function reset last_attack_bonus in player
                node.move_bonus_to_mine()
                self.__curr_bonus_node = node

                if node.can_attack():
                    if limit > 0:
                        curr_copy = deepcopy(self)
                        ret_states.append(curr_copy)
                        limit -= 1
                else:
                    # can't attack although we added bonus
                    max_loss = node.max_loss_attack()
                    if max_loss > case2_diff:
                        case2_diff = max_loss
                        case2 = node
                node.undo_move_bonus_to_mine()
                self.__curr_bonus_node = None

        # add case1
        if case1:
            case1.move_bonus_to_mine()
            ret_states.append(deepcopy(self))
            case1.set_army(case1.get_army - curr_bonus)

        if case2:
            # add case2
            case2.move_bonus_to_mine()
            ret_states.append(deepcopy(self))
            case2.set_army(case1.get_army - curr_bonus)

        return ret_states

    """
        limit the branching factor y using limit argument.
        choose one of the possible limiting branching:
            - limit the branching by choosing the pair of nodes which make the attacker have largest remaining armies
            - limit the branching by choosing the pair of nodes which has the lease difference so we start with them as 
               we may not be able to attack that node later as it can be stronger, so attack ot now as soos as you can.
        divide_armies to limit possible moves from ther attacker node to the attacked node
    """
    def expand_attack(self, state, limit=maxsize, largest_remaining_heuristic=True, minimum_difference_heuristic=False, divide_armies=True):
        # to make priority of branches to support limit
        # priority queue pop the max priority
        pq = []
        attacker_nodes = self.get_current_player().get_border_nodes()
        for attacker_node in attacker_nodes:
            attacked_nodes = attacker_node.get_possible_attacked_nodes()
            for attacked_node in attacked_nodes:
                possible_armies_movies = list()
                # just move one army to the attacked node
                possible_armies_movies.append(1)
                # just keep one army in the attacker node
                possible_armies_movies.append(attacker_node.get_army() - attacked_node.get_army() - 1)
                # divide the armies between the nodes
                if divide_armies:
                    # first possible divide in favor of attacker node to increase its chance of attack later
                    neighbour_nodes = attacker_node.get_neighbours()
                    remaining_armies = attacker_node.get_army() - attacked_node.get_army()
                    opponent_bonus = self.get_next_player().get_bonus()
                    min_army_needed_in_attacker_node = maxsize
                    for neighbour in neighbour_nodes:
                        if neighbour.get_node_name() == attacked_node.get_node_name() \
                                or neighbour.get_hold_player() == self.get_current_player():
                            continue
                        min_army_needed_in_attacker_node = min(min_army_needed_in_attacker_node, \
                                                               neighbour.get_army() + opponent_bonus + 2)
                    if not(min_army_needed_in_attacker_node >= remaining_armies - 1):
                        possible_armies_movies.append(remaining_armies - min_army_needed_in_attacker_node)

                    # second possible divide in favor of attacker node to increase its chance of attack later
                    neighbour_nodes = attacked_node.get_neighbours()
                    remaining_armies = attacker_node.get_army() - attacked_node.get_army()
                    opponent_bonus = self.get_next_player().get_bonus()
                    min_army_needed_in_attacked_node = maxsize
                    for neighbour in neighbour_nodes:
                        if neighbour.get_hold_player() == self.get_current_player():
                            continue
                        min_army_needed_in_attacked_node = min(min_army_needed_in_attacked_node, \
                                                               neighbour.get_army() + opponent_bonus + 2)
                    if not(min_army_needed_in_attacked_node >= remaining_armies - 1):
                        possible_armies_movies.append(min_army_needed_in_attacked_node)

                # tuple (priority, my object)
                obj = ()
                attack_move = list()
                attack_move.append(attacker_node.get_node_name())
                attack_move.append(attacked_node.get_node_name())
                attack_move.append(1)
                if minimum_difference_heuristic:
                    for moved_armies in possible_armies_movies:
                        attack_move[2] = moved_armies
                        obj = (-1 * (attacker_node.get_army() - attacked_node.get_army()), attack_move)
                        heappush(pq, obj)

                else:
                    for moved_armies in possible_armies_movies:
                        attack_move[2] = moved_armies
                        obj = (attacker_node.get_army() - attacked_node.get_army(), attack_move)
                        heappush(pq, obj)

        next_states = []
        for i in range(0, limit):
            # get the best ith attack move
            attack_move = heappop(pq)[1]
            curr_state_copy = deepcopy(self)
            attacker_node = curr_state_copy.get_current_player().get_node_by_name(attack_move[0])
            attacked_node = curr_state_copy.get_next_player().get_node_by_name(attack_move[1])
            moved_armies = attack_move[2]
            # apply the attack move and get the next state
            move = Move()
            move.set_attacker_node(attacker_node)
            move.set_attacked_node(attacked_node)
            move.set_attacked_node_armies(moved_armies)
            move.apply_move()
            next_states.append(curr_state_copy)
        return next_states