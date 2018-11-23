from sys import maxsize


class Node:

    def __int__(self, node_name, hold_player, army, neighbours, partition):
        self.__node_name = node_name
        self.__hold_player = hold_player
        self.__army = army
        self.__neighbours = neighbours
        self.__partition = partition

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
    def set_partition(self, partition):
        self.__partition = partition

    @property
    def set_node_name(self, node_name):
        self.__node_name = node_name

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
    def get_partition(self):
        return self.__partition

    @property
    def get_node_name(self):
        return self.__node_name

    def can_attack(self):
        for node in self.__neighbours:
            if self.can_attack(node):
                return True
        return False

    def max_loss_attack(self):
        max_loss = -1 * maxsize
        for node in self.__neighbours:
            if self.__hold_player != node.get_hold_player():
                max_loss = max(max_loss, self.__army - node.get_army)
        return max_loss

    def min_loss_attack(self):
        min_loss = maxsize
        for node in self.__neighbours:
            if self.__hold_player != node.get_hold_player():
                min_loss = min(min_loss, self.__army - node.get_army)
        return min_loss


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
            self.__hold_player.add_node(node)
            # player successfully attacked so he will get 2 bonus on the next turn
            self.__hold_player.set_last_attack_bonus(2)
            return True
        else:
            return False

    # return status of moving arimes to another node [success of failure]
    # neighbour_condition to make constraint on moving armies to neighbouring nodes only
    # armies represent number of armies we want to move from the current node to node
    def move_army_to_another_node(self, armies, node, neighbour_condition=True):
        cond = True
        if neighbour_condition:
            cond = cond and (node in self.__neighbours)
        if cond and (self.__hold_player == node.get_hold_player()) and (self.get_army() > armies):
            self.set_army(self.get_army() - armies)
            node.set_army(node.get_army() + armies)
            return True
        else:
            return False


    def undo_move_bonus_to_mine(self):
        self.__hold_player.set_last_attack_bonus(2)
        self.__army -= self.__hold_player.get_bonus()


    def move_bonus_to_mine(self):
        bonus = self.__hold_player.get_bonus()
        self.__army += bonus
        self.__hold_player.set_last_attack_bonus(0)

    def get_possible_attacked_nodes(self):
        possible_attacked_nodes = []
        for node in self.__neighbours:
            if self.can_attack(node):
                possible_attacked_nodes.append(node)
        return possible_attacked_nodes

    def get_possible_attacked_node_by_name(self, node_number):
        nodes = self.get_possible_attacked_nodes()
        for node in nodes:
            if node.get_node_name() == node_number:
                return node
        return None
