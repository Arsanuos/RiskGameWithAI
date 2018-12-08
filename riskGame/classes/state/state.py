from copy import deepcopy
from sys import maxsize
from heapq import *
from riskGame.classes.state.move import Move
from riskGame.classes.evaluations.sigmoidEval import SigmoidEval
import random

class State:

    def __init__(self, number_nodes, partitions, players, player_turn_number):
        self.__number_nodes = number_nodes
        self.__partitions = partitions
        self.__players = players
        self.__player_turn_number = player_turn_number
        self.__turn_number = 0
        # TODO check -1 is invalid value for hash string
        self.__hashed_value = -1
        self.__parent_state = None

    def set_players(self, players):
        self.__players = players

    def set_number_nodes(self, number_nodes):
        self.__number_nodes = number_nodes

    def set_partitions(self, partitions):
        self.__partitions = partitions

    def set_player_turn_number(self, player_turn_number):
        self.__player_turn_number = player_turn_number

    def set_turn_number(self, turn_number):
        self.__turn_number = turn_number

    def set_parent_state(self, parent_state):
        self.__parent_state = parent_state

    def get_players(self):
        return self.__players

    def get_number_nodes(self):
        return self.__number_nodes

    def get_partitions(self):
        return self.__partitions

    def get_player_turn_number(self):
        return self.__player_turn_number

    def get_turn_number(self):
        return self.__turn_number

    def get_parent_state(self):
        return self.__parent_state

    def increase_turn(self):
        self.__turn_number += 1

    def calculate_gn(self, initial_state):
        return self.__turn_number - initial_state.get_turn_number()

    def get_current_player(self):
        return self.__players[self.__player_turn_number]

    def get_next_player(self):
        return self.__players[(self.__player_turn_number + 1) % len(self.__players)]

    def increase_player_turn(self):
        self.__player_turn_number += 1
        self.__player_turn_number %= len(self.__players)

    def get_winner(self):
        for player in self.__players:
            if len(player.get_hold_nodes()) == self.__number_nodes:
                return player
        return None

    def expand_bonus(self, limit=maxsize):
        if self.get_current_player().get_bonus() == 0:
            return []
        curr_player = self.get_current_player()

        # get border nodes
        border_nodes = curr_player.get_border_nodes()

        no_need_bonus = []
        need_more_bonus = []
        need_bonus = []

        for node in border_nodes:
            # copy my now state
            copied_state = deepcopy(self)
            # get the node that look like my current holding node.
            copied_node = copied_state.get_current_player().get_node_by_name(node.get_node_name())

            # node can attack without even use bonus
            if len(copied_node.get_possible_attacked_nodes()) > 0:
                # already has more troops
                no_need_bonus.append(copied_node)
            else:
                copied_node.set_army(copied_node.get_army() + copied_state.get_current_player().get_bonus())
                if len(copied_node.get_possible_attacked_nodes()) > 0:
                    need_bonus.append((copied_node, maxsize * -1))
                else:
                    # can't attack although we added bonus
                    need_more_bonus.append(copied_node)
                copied_node.set_army(copied_node.get_army() - copied_state.get_current_player().get_bonus())

        # priority for no_need_bonus
        sorted_no_need_bonus = []
        for node in no_need_bonus:
            # score = loss if node attacked weakest node.
            val = node.min_loss_attack()
            sorted_no_need_bonus.append((node, val))
        sorted_no_need_bonus = sorted(sorted_no_need_bonus, key=lambda x: x[1])

        # priority for need_more_bonus
        sorted_need_more_bonus = []
        for node in need_more_bonus:
            # score = loss if node attacked weakest node
            val = node.min_loss_attack()
            sorted_need_more_bonus.append((node, -val))
            sorted_need_more_bonus = sorted(sorted_need_more_bonus, key=lambda x: x[1])

        ret_nodes = need_bonus + sorted_need_more_bonus + sorted_no_need_bonus

        next_moves = []
        nodes = ret_nodes[:min(limit, len(ret_nodes))]
        for node in nodes:
            move = Move()
            move.set_bonus_hold_node(node[0])
            next_moves.append(move)
        return next_moves

    """
        limit the branching factor y using limit argument.
        choose one of the possible limiting branching:
            - limit the branching by choosing the pair of nodes which make the attacker have largest remaining armies
            - limit the branching by choosing the pair of nodes which has the lease difference so we start with them as 
               we may not be able to attack that node later as it can be stronger, so attack ot now as soos as you can.
        divide_armies to limit possible moves from ther attacker node to the attacked node
    """
    def expand_attack(self, limit=maxsize, largest_remaining_heuristic=True, minimum_difference_heuristic=False, divide_armies=True):
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
                sign = 1
                if minimum_difference_heuristic:
                    sign = -1
                if largest_remaining_heuristic:
                    sign = 1
                for moved_armies in possible_armies_movies:
                    attack_move = list()
                    attack_move.append(attacker_node.get_node_name())
                    attack_move.append(attacked_node.get_node_name())
                    attack_move.append(moved_armies)
                    obj = (sign * (attacker_node.get_army() - attacked_node.get_army()), attack_move)
                    heappush(pq, obj)

        next_states = []
        sz = len(pq)
        for i in range(0, min(limit, sz)):
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
            #move.apply_move()
            next_states.append(move)
        return next_states

    def expand_move(self, limit=maxsize):
        """
        expand all possible moves (the most important ones). the most important nodes are defined as follow:
            - from the borders to the nearest non-border node that have an army > 1 consider that node to be source of
                and the target will be the current bordering node.
            - the case when target node (non-border) is the same for two or more border node then consider each cases.
            - use BFS to get the nearest
        :return: all possible moves to be bundled after that with attack and bonus moves.
        """

        pq = []
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
                move.set_moved_armies(new_nearest_node.get_army() - 1)
                next_states.append(move)

        if len(next_states) > 0:
            return next_states

        temp_states = []
        for node in all_nodes:
            childs = node.get_neighbours()
            for child in childs:
                if child.get_hold_player().get_name() == self.get_current_player().get_name():
                    try_armies = [node.get_army() - 1]
                    for armies in try_armies:
                        if node.can_move_to_another_node(armies, child):
                            new_state = deepcopy(self)
                            new_node = new_state.get_current_player().get_node_by_name(node.get_node_name())
                            new_child = new_state.get_current_player().get_node_by_name(child.get_node_name())
                            move = Move()
                            move.set_move_from_node(new_node)
                            move.set_move_to_node(new_child)
                            move.set_moved_armies(armies)
                            move_obj = list()
                            move_obj.append(new_node.get_node_name())
                            move_obj.append(new_child.get_node_name())
                            move_obj.append(armies)
                            temp_states.append(move)

        if len(next_states) == 0:
            for i in range(0, min(3, len(temp_states))):
                next_states.append(temp_states[i])
        return next_states


    def expand(self):
        bonus_moves = self.expand_bonus(limit=4)
        move_moves = self.expand_move(4)
        attack_moves = self.expand_attack(limit=4, divide_armies=False)
        total_states = max(len(bonus_moves), 1) * max(len(move_moves), 1) * max(len(attack_moves), 1)
        if len(bonus_moves) == 0 and len(move_moves) == 0 and len(attack_moves) == 0:
            total_states = 0
        print('Expand state to {} states'.format(total_states))
        next_states = []
        if len(bonus_moves) == 0: bonus_moves.append(None)
        if len(move_moves) == 0: move_moves.append(None)
        if len(attack_moves) == 0: attack_moves.append(None)
        for move1 in bonus_moves:
            for move2 in move_moves:
                for move3 in attack_moves:
                    copied_state = deepcopy(self)
                    bonus_node = None
                    if move1:
                        bonus_node = copied_state.get_current_player().get_node_by_name(move1.get_bonus_hold_node().get_node_name())
                    move_from_node = move_to_node = moved_armies = None
                    if move2:
                        move_from_node = copied_state.get_current_player().get_node_by_name(move2.get_move_from_node().get_node_name())
                        move_to_node = copied_state.get_current_player().get_node_by_name(move2.get_move_to_node().get_node_name())
                        moved_armies = move2.get_moved_armies()
                    attacker_node = attacked_node = attacked_armies = None
                    if move3:
                        attacker_node = copied_state.get_current_player().get_node_by_name(move3.get_attacker_node().get_node_name())
                        attacked_node = copied_state.get_next_player().get_node_by_name(move3.get_attacked_node().get_node_name())
                        attacked_armies = move3.get_attacked_node_armies()
                    move = Move()
                    move.set_bonus_hold_node(bonus_node)
                    move.set_move_from_node(move_from_node)
                    move.set_move_to_node(move_to_node)
                    move.set_moved_armies(moved_armies)
                    move.set_attacker_node(attacker_node)
                    move.set_attacked_node(attacked_node)
                    move.set_attacked_node_armies(attacked_armies)
                    move.apply_move()
                    copied_state.increase_turn()
                    copied_state.increase_player_turn()
                    copied_state.reset_hash()
                    copied_state.set_parent_state(self)
                    next_states.append(copied_state)
        return next_states

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
        vis = set()
        d = 0
        all_nodes = set(all_nodes)
        border_nodes = set(border_nodes)
        while len(q):
            s = len(q)
            node, parent = q.pop(0)
            d += 1
            if d > max_depth:
                return (None, None)
            while s:
                s -= 1
                if (node not in vis) and (node not in border_nodes or node.get_node_name() == start_node.get_node_name()):
                    vis.add(node)
                    if node in all_nodes and node not in border_nodes and node.get_army() > 1:
                        return (node, parent)
                    for child in node.get_neighbours():
                        q.append((child, node))
        # can be reached if all nodes is either border or has army less than or equal 1.
        return (None, None)

    def get_steps_to_root(self):
        temp_state = self
        all_states = []
        while temp_state:
            all_states.append(temp_state)
            temp_state = temp_state.get_parent_state()
        all_states = all_states[:-1]
        return all_states[::-1]

    def to_array(self):
        arr = []
        for player in self.__players:
            arr.append(player.get_bonus())
        all_nodes = []
        for player in self.__players:
            for node in player.get_hold_nodes():
                all_nodes.append((node, node.get_node_name()))
        all_nodes = sorted(all_nodes, key=lambda x: x[1])
        for node in all_nodes:
            arr.append((node[0].get_hold_player().get_name(), node[0].get_army()))
        return arr

    def print_state(self):
        print("State = " + str(self.to_array()))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        if self.__hashed_value == -1:
            self.__hashed_value = hash(str(self.to_array()))
        return self.__hashed_value

    def reset_hash(self):
        self.__hashed_value = -1

    def __lt__(self, other):
        return self.get_turn_number() < other.get_turn_number()
