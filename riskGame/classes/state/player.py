class Player:

    def __int__(self, name, hold_nodes):
        self.__name = name
        self.__hold_nodes = hold_nodes
        self.__last_attack_bonus = 0

    @property
    def set_name(self, name):
        self.__name = name

    @property
    def set_hold_nodes(self, hold_nodes):
        self.__hold_nodes = hold_nodes

    @property
    def set_last_attack_bonus(self, last_attack_bonus):
        self.__last_attack_bonus = last_attack_bonus

    @property
    def get_name(self):
        return self.__name

    @property
    def get_hold_nodes(self):
        return self.__hold_nodes

    @property
    def get_last_attack_bonus(self):
        return self.__last_attack_bonus

    def add_node(self, node):
        self.__hold_nodes.append(node)
        node.set_hold_player(self)

    def remove_node(self, node):
        self.__hold_nodes.remove(node)
        node.set_hold_player(None)

    def calculate_partition_bonus(self):
        unique_partitions = set()
        partition_list = []
        for node in self.__hold_nodes:
            partition_number = node.get_partition().get_partition_number()
            if partition_number in unique_partitions:
                continue
            unique_partitions.add(partition_number)
            partition_list.append(node.get_partition())

        bonus = 0
        for partition in partition_list:
            flag = True
            for node in partition.get_nodes():
                if node not in self.__hold_nodes:
                    flag = False
                    break
            if flag:
                bonus += partition.get_partition_bonus()

        return bonus

    def get_bonus(self):
        return self.calculate_partition_bonus() + self.__last_attack_bonus
