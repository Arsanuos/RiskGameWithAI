from copy import deepcopy
from sys import maxsize



class State:

    def __init__(self, number_nodes, partitions, players, player_turn_number):
        self.__number_nodes = number_nodes
        self.__partitions = partitions
        self.__players = players
        self.__player_turn_number = player_turn_number

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

    def get_winner(self):
        for player in self.__players:
            if len(player.get_hold_nodes()) == self.__number_nodes:
                return player
        return None

    def expand_bonus(self):
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
                node.move_bonus_to_mine()
                if node.can_attack():
                    curr_copy = deepcopy(self)
                    ret_states.append(curr_copy)
                else:
                    # can't attack although we added bonus
                    max_loss = node.max_loss_attack()
                    if maxsize > case2_diff:
                        case2_diff = maxsize
                        case2 = node
                node.set_army(node.get_army - curr_bonus)

        # add case1
        case1.move_bonus_to_mine()
        ret_states.append(deepcopy(self))
        case1.set_army(case1.get_army - curr_bonus)

        # add case2
        case2.move_bonus_to_mine()
        ret_states.append(deepcopy(self))
        case2.set_army(case1.get_army - curr_bonus)

        return ret_states
