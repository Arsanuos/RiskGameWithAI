class Move:

    def __init__(self):
        self.__bonus_hold_node = None
        self.__attacker_node = None
        self.__attacked_node = None
        self.__attacked_node_armies = None
        self.__move_from_node = None
        self.__move_to_node = None
        self.__moved_armies = None

    @property
    def set_bonus_hold_node(self, bonus_hold_node):
        self.__bonus_hold_node = bonus_hold_node

    @property
    def set_attacker_node(self, attacker_node):
        self.__attacker_node = attacker_node

    @property
    def set_attacked_node(self, attacked_node):
        self.__attacked_node = attacked_node

    @property
    def set_attacked_node_armies(self, attacked_node_armies):
        self.__attacked_node_armies = attacked_node_armies

    @property
    def set_move_from_node(self, move_from_node):
        self.__move_from_node = move_from_node

    @property
    def set_move_to_node(self, move_to_node):
        self.__move_to_node = move_to_node

    @property
    def set_moved_armies(self, moved_armies):
        self.__moved_armies = moved_armies

    @property
    def get_bonus_hold_node(self):
        return self.__bonus_hold_node

    @property
    def get_attacker_node(self):
        return self.__attacker_node

    @property
    def get_attacked_node(self):
        return self.__attacked_node

    @property
    def get_attacked_node_armies(self):
        return self.__attacked_node_armies

    @property
    def get_move_from_node(self):
        return self.__move_from_node

    @property
    def get_move_to_node(self):
        return self.__move_to_node

    @property
    def get_moved_armies(self):
        return self.__moved_armies

    # called after setting all the attributes
    def apply_move(self):
        # apply bonus
        if self.__bonus_hold_node:
            self.__bonus_hold_node.move_bonus_to_mine()
        # apply move armies
        if self.__move_from_node:
            self.__move_from_node.move_army_to_another_node(self.__moved_armies, self.__move_to_node)
        # apply attack
        if self.__attacker_node:
            self.__attacker_node.attack(self.__attacked_node, self.__attacked_node_armies)