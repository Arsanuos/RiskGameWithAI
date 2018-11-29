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
            copied_state = deepcopy(self)
            copied_node = copied_state.get_current_player().get_node_by_name(node.get_node_name())
            if copied_node.can_attack():
                # already has more troops
                min_loss = copied_node.min_loss_attack()
                if min_loss < case1_diff:
                    case1_diff = min_loss
                    case1 = (copied_node, copied_state)
            else:
                copied_node.move_bonus_to_mine()
                if copied_node.can_attack():
                    if limit > 0:
                        ret_states.append(copied_state)
                        limit -= 1
                else:
                    # can't attack although we added bonus
                    max_loss = copied_node.max_loss_attack()
                    if max_loss > case2_diff:
                        case2_diff = max_loss
                        case2 = (copied_node, copied_state)
        # add case1
        if case1:
            case1[0].move_bonus_to_mine()
            ret_states.append(case1[1])

        if case2:
            # add case2
            ret_states.append(case2[1])

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

    def expand_move(self):
        """
        expand all possible moves (the most important ones). the most important nodes are defindes as follows:
            - from the borders to the nearest non-border node that have an army > 1 consider that node to be source of
                and the target will be the current bordering node.
            - the case when target node (non-border) is the same for two or more border node then consider each cases.
            - use BFS to get the nearest
        :return: all possible moves to be bundled after that with attack and bonus moves.
        """
        next_states = []
        cur_player = self.get_current_player()
        border_nodes = cur_player.get_border_nodes()
        all_nodes = cur_player.get_hold_nodes()
        for node in border_nodes:
            nearest_node, parent = self.BFS(node, all_nodes, border_nodes, len(all_nodes) + 1)
            if nearest_node is not None and parent is not None:
                new_state = deepcopy(self)
                new_nearest_node = new_state.get_current_player().get_node_by_name(nearest_node.get_node_name())
                new_parent = new_state.get_current_player().get_node_by_name(parent.get_node_name())
                move = Move()
                move.set_move_from_node(new_nearest_node)
                move.set_move_to_node(new_parent)
                move.apply_move()
                next_states.append(new_state)
        return new_state

    ## UTILS ##
    def BFS(self, start_node, all_nodes, border_nodes, max_depth):
        """
            get start node, all nodes and border_nodes as the target
            node must be on of the all_nodes and not one of the border_nodes and has army > 1.
        :param start_node:
        :param all_nodes:
        :param border_nodes:
        :param max_depth:
        :return:
        """
        q = []
        q.append((start_node, None))
        vis = []
        d = 0
        while len(q):
            s = len(q)
            node, parent = q.pop(0)
            d += 1
            if d > max_depth:
                return (None, None)
            while s:
                s -= 1
                if node not in vis and node not in border_nodes:
                    vis.add(node)
                    if node in all_nodes and node not in border_nodes and node.get_army() > 1:
                        return (node, parent)
                    for child in node.get_neighbours():
                        q.append((child, node))
        # can be reached if all nodes is either border or has army less than or equal 1.
        return (None, None)