

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
            Do we need further implementation of the way a graph will look like 
            (edge list, adj matrix, ...) or every one will implement it as he needs.
            
            No, same Implementation.
            """
            #Assuming Edge is a tuple of (start, end)
            for edge in edges:
                nodes[edge[0]].add_neighbor(nodes[edge[1]])
                nodes[edge[1]].add_neighbor(nodes[edge[0]])

