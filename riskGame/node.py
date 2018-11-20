
class Node:

    def __int__(self, hold_player, army, neighbours, partition_number):
        self.__hold_player = hold_player
        self.__army = army
        self.__neighbours = neighbours
        self.__partition_number = partition_number

    @property
    def set_army(self, army):
        self.__army = army

    @property
    def set_neighbours(self, neighbours):
        self.__neighbours = neighbours

    @property
    def set_hold_player(self, hold_player):
        self.__hold_player = hold_player

    @property
    def set_partition_number(self, partition_number):
        self.__partition_number = partition_number

    @property
    def get_army(self):
        return self.__army

    @property
    def get_neighbours(self):
        return self.__neighbours

    @property
    def get_hold_player(self):
        return self.__hold_player

    @property
    def get_partition_number(self):
        return self.__partition_number

    # check if we can attach the node from current node
    def can_attack(self, node):
        if (node in self.__neighbours) and (self.__hold_player != node.get_hold_player()) \
                and (self.__army - node.get_army() > 1):
            return True
        return False

    # return true if we can attack the node, As a result update the nodes after attack
    # return false if we can't attack the node, As a result no updates will be done
    # moved_army argument is the number of armies will be moved to the attacked node, default = 1
    def attack(self, node, moved_army=1):
        if self.can_attack(node):
            node.get_hold_player().remove_node(node)
            self.set_army(max(self.__army - node.get_army() - moved_army, 1))
            node.set_army(moved_army)
            self.get_hold_player().add_node(node)
            return True
        else:
            return False

