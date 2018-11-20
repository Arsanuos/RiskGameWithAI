class Player:

    def __int__(self, name, hold_nodes, bonus):
        self.__name = name
        self.__hold_nodes = hold_nodes
        self.__bonus = bonus

    @property
    def set_name(self, name):
        self.__name = name

    @property
    def set_bonus(self, bonus):
        self.__bonus = bonus

    @property
    def set_hold_nodes(self, hold_nodes):
        self.__hold_nodes = hold_nodes

    @property
    def get_name(self):
        return self.__name

    @property
    def get_bonus(self):
        return self.__bonus

    @property
    def get_hold_nodes(self):
        return self.__hold_nodes

    def add_node(self, node):
        self.__hold_nodes.append(node)
        node.set_hold_player(self)

    def remove_node(self, node):
        self.__hold_nodes.remove(node)
        node.set_hold_player(None)