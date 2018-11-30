class Player:

    def __init__(self, name, hold_nodes):
        self.__name = name
        self.__hold_nodes = hold_nodes
        self.__last_attack_bonus = 0
        self.__nodes_dic = {node.get_node_name() : node for node in self.__hold_nodes}

    def set_name(self, name):
        self.__name = name

    def set_hold_nodes(self, hold_nodes):
        self.__hold_nodes = hold_nodes
        self.__nodes_dic = {node.get_node_name() : node for node in self.__hold_nodes}

    def set_last_attack_bonus(self, last_attack_bonus):
        self.__last_attack_bonus = last_attack_bonus

    def get_name(self):
        return self.__name

    def get_hold_nodes(self):
        return self.__hold_nodes

    def get_last_attack_bonus(self):
        return self.__last_attack_bonus

    def add_node(self, node):
        self.__hold_nodes.append(node)
        node.set_hold_player(self)
        self.__nodes_dic[node.get_node_name()] = node

    def remove_node(self, node):
        ids = [node_x.get_node_name() for node_x in self.__hold_nodes]
        for idx, id in enumerate(ids):
            if id == node.get_node_name():
                self.__hold_nodes.pop(idx)
        node.set_hold_player(None)
        del self.__nodes_dic[node.get_node_name()]

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
        my_nodes = [x.get_node_name() for x in self.__hold_nodes]
        for partition in partition_list:
            flag = True
            for node in partition.get_nodes():
                if node.get_node_name() not in my_nodes:
                    flag = False
                    break
            if flag:
                bonus += partition.get_partition_bonus()

        return bonus

    def get_bonus(self):
        return self.calculate_partition_bonus() + self.__last_attack_bonus

    def get_node_by_name(self, node_number):
        """
        for node in self.__hold_nodes:
            if node.get_node_name() == node_number:
                return node
        """
        # faster way using dictionary
        if node_number not in self.__nodes_dic:
            return None
        return self.__nodes_dic[node_number]

    def get_border_nodes(self):
        border_nodes = []
        for node in self.__hold_nodes:
            neighbors = node.get_neighbours()
            for neighbor in neighbors:
                if neighbor not in self.__hold_nodes:
                    border_nodes.append(node)
                    break
        return border_nodes
