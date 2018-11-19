

class State:

    def __init__(self, nodes, edges):
        self.__construct_graph(nodes, edges)

    @property
    def get_nodes(self):
        return self.__nodes

    @property
    def get_edges(self):
        return self.__edges

    @property
    def set_nodes(self, nodes):
        self.__nodes = nodes

    @property
    def set_edges(self, edges):
        self.__edges = edges


def __construct_graph(self, nodes, edges):
        self.__nodes = nodes
        self.__edges = edges
        """
        Do we need further impelementation of the way a graph will look like 
        (edge list, adj matrix, ...) or every one will implement it as he needs.
        """

