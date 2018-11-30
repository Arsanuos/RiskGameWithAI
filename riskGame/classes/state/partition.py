class Partition:

    def __init__(self, partition_number, nodes, partition_bonus):
        self.__partition_number = partition_number
        self.__nodes = nodes
        self.__partition_bonus = partition_bonus

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def set_partition_bonus(self, partition_bonus):
        self.__partition_bonus = partition_bonus

    def set_partition_number(self, partition_number):
        self.__partition_number = partition_number

    def get_nodes(self):
        return self.__nodes

    def get_partition_bonus(self):
        return self.__partition_bonus

    def get_partition_number(self):
        return self.__partition_number
