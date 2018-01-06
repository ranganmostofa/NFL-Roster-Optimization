from Edge import Edge
from GraphProcessing import GraphProcessing


class AdjacencyMatrix:
    """
    General-purpose AdjacencyMatrix class for the BipartiteGraph module
    """
    def __init__(self, nodes, adjacency_matrix):
        """
        Constructor for the AdjacencyMatrix class - used to initialize all necessary fields of the
        AdjacencyMatrix object
        """
        self.nodes = nodes  # initialize all necessary fields
        self.adjacency_matrix = adjacency_matrix

        self.__check_validity()  # check if graph is valid - throws exception if not

    def __str__(self):
        """
        Returns a neatly formatted string representation of the BipartiteGraph object
        """
        # string representation includes values of all inner fields
        return "Nodes: " + "\n" + "\n".join([node.__str__() for node in self.nodes]) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the AdjacencyMatrix object
        """
        return hash(str(self))  # return the hashcode

    def __eq__(self, other):
        """
        Given an AdjacencyMatrix object, checks whether this AdjacencyMatrix object is equal to the input
        AdjacencyMatrix object - equality of two AdjacencyMatrix objects is defined in terms of equality
        of inner fields and not as identical objects in memory
        """
        # check equality of nodesets
        return \
            set(self.get_node_names()).__eq__(set(other.get_node_names())) and \
            set(self.get_edges_as_node_name_pairs()).__eq__(set(other.get_edges_as_node_name_pairs()))

    def __deepcopy__(self):
        """
        Creates and returns a deepcopy of the current AdjacencyMatrix object - all internal nodes and edges
        and their respective internal fields are replicated without invoking an infinite recursive call
        """
        A_prime = AdjacencyMatrix(list(), list())  # initialize an empty AdjacencyMatrix object

        # populate the empty nodeset with duplicate disconnected copies of nodes from the original adjacency matrix
        for node in self.nodes: A_prime.add_node(GraphProcessing.produce_duplicate_disconnected_node(node))

        # for each edge in the original graph
        for edge in self.get_edges():
            A_prime.add_edge(
                edge.get_weight(),
                dict(edge.get_attributes()),
                GraphProcessing.search_node_names(set(A_prime.get_nodes()), edge.get_source_node().get_name()).pop(),
                GraphProcessing.search_node_names(set(A_prime.get_nodes()), edge.get_terminal_node().get_name()).pop()
            )  # add a duplicate edge to the new graph

        return A_prime  # return the new duplicate adjacency matrix

    def add_node_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of the Node objects in the graph
        """
        A_prime = self.__deepcopy__()  # create a deepcopy of the adjacency matrix
        for node in A_prime.get_nodes():  # for every node in the graph
            # add the attribute key-value pair to the attributes registry of the node
            node.add_attribute(attribute_key, attribute_value)
        return A_prime  # return the modified adjacency matrix

    def add_edge_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of Edge objects in the graph
        """
        A_prime = self.__deepcopy__()  # create a deepcopy of the adjacency matrix
        for edge in A_prime.get_edges():  # for every edge in the graph
            # add the attribute key-value pair to the attributes registry of the edge
            edge.add_attribute(attribute_key, attribute_value)
        return A_prime  # return the modified adjacency matrix

    def add_node(self, node):
        """
        Given a Node object, adds the input to the list of Node objects and expands the adjacency matrix to
        accommodate the new node
        """
        self.nodes.append(node)  # append the input node object to the list of nodes

        # add an empty row to the adjacency matrix - this row should contain edges originating from the new node
        self.adjacency_matrix.append(list())

        # populate the empty row initialized above with placeholder edges
        for index in range(len(self.adjacency_matrix) - 1):
            terminal_node = self.nodes[index]
            self.adjacency_matrix[len(self.adjacency_matrix) - 1].append(Edge(0, dict(), node, terminal_node))

        # add a column of placeholder edges leading to the new node
        for row_index in range(len(self.adjacency_matrix)):
            source_node = self.nodes[row_index]
            self.adjacency_matrix[row_index].append(Edge(0, dict(), source_node, node))

        self.__check_validity()  # check if graph is valid - throws exception if not

    def add_edge(self, weight, attributes, source_node, terminal_node):
        """
        Given the necessary inner fields of an Edge object, creates the Edge object and connects the
        source and terminal nodes using this edge
        """
        # if the source node is not in the set of nodes
        if source_node.get_name() not in self.get_node_names():
            self.add_node(source_node)  # add the source node

        # if the terminal node is not in the set of nodes
        if terminal_node.get_name() not in self.get_node_names():
            self.add_node(terminal_node)  # add the terminal node

        edge = Edge(weight, dict(attributes), source_node, terminal_node)  # create the Edge object

        source_node.add_outgoing_edge(edge)  # connect the source node and the terminal node using the edge
        terminal_node.add_incoming_edge(edge)

        # add the edge to the adjacency matrix
        source_node_index = self.get_node_names().index(source_node.get_name())
        terminal_node_index = self.get_node_names().index(terminal_node.get_name())
        self.adjacency_matrix[source_node_index][terminal_node_index] = edge

        self.__check_validity()  # check if graph is valid - throws exception if not

    def get_nodes(self):
        """
        Returns a list of nodes in the graph represented by the adjacency matrix
        """
        return list(self.nodes)  # return the list of nodes

    def get_node_names(self):
        """
        Returns a list of node names in the graph represented by the adjacency matrix
        """
        return list([node.get_name() for node in self.nodes])  # return the list of node names

    def get_adjacency_matrix(self):
        """
        Returns the adjacency matrix of the graph
        """
        return list([list(row) for row in self.adjacency_matrix])  # return the adjacency matrix

    def get_edges(self):
        """
        Returns a set of the edges in the graph represented by the adjacency matrix
        """
        return {edge for row in list(self.adjacency_matrix) for edge in list(row)}  # return the set of edges

    def get_edges_as_node_name_pairs(self):
        """
        Returns a set of the edges (as pairs of node names) in the graph represented by the adjacency matrix
        """
        return \
            set(
                {
                    tuple((edge.get_source_node().get_name(), edge.get_terminal_node().get_name()))
                    for edge in self.get_edges()
                }
            )  # return the set of edges

    def set_nodes(self, nodes):
        """
        Given a list of Node objects, sets the current list of nodes in the graph as the input
        """
        self.nodes = list(nodes)  # overwrite the current list of nodes with the input

        self.__check_validity()  # check if graph is valid - throws exception if not

    def set_adjacency_matrix(self, adjacency_matrix):
        """
        Given an adjacency matrix represented as a list of lists of Edge objects, sets the adjacency matrix
        of the graph as the input
        """
        # overwrite the current adjacency matrix with the input
        self.adjacency_matrix = list([list(row) for row in adjacency_matrix])

        self.__check_validity()  # check if graph is valid - throws exception if not

    @staticmethod
    def bipartite_to_adjacency_matrix_form(G):
        """
        Given a BipartiteGraph object, returns an adjacency matrix representation of the input graph using
        doubly nested lists
        """
        A = AdjacencyMatrix(list(), list())  # initialize an empty AdjacencyMatrix object

        # populate the empty nodeset with duplicate disconnected copies of nodes from the input bipartite graph
        for node in G.get_left_nodeset().union(G.get_right_nodeset()):
            A.add_node(GraphProcessing.produce_duplicate_disconnected_node(node))

        # for each edge in the input bipartite graph
        for edge in G.get_edges():
            A.add_edge(
                edge.get_weight(),
                dict(edge.get_attributes()),
                GraphProcessing.search_node_names(set(A.get_nodes()), edge.get_source_node().get_name()).pop(),
                GraphProcessing.search_node_names(set(A.get_nodes()), edge.get_terminal_node().get_name()).pop()
            )  # add a duplicate edge to the new graph

        return A  # return the adjacency matrix form of the input bipartite graph

    def __has_conflicting_node_names(self):
        """
        Returns True if the graph nodes have conflicting names and False otherwise
        """
        # check length of list and set to determine if overlap exists
        return len(list(self.get_node_names())) != len(set(self.get_node_names()))

    def __has_incompatible_matrix_dimensions(self):
        """
        Returns True if the adjacency matrix is of size n x n the length of the nodes list is m where m is
        not equal to n and False otherwise
        """
        # return True if the length of the nodes list is not equal to the number of rows in the adjacency matrix
        if len(self.nodes) != len(self.adjacency_matrix): return True

        # return True if the length of the nodes list is not equal to the length of the rows in the adjacency matrix
        for row in self.adjacency_matrix:
            if len(self.nodes) != len(list(row)):
                return True

        return False  # if all tests have passed, return False

    def __check_validity(self):
        """
        Throws an exception if:

        (1) Nodes have conflicting names
        (2) Nodes list and adjacency matrix have incompatible dimensions

        Method should be called after every mutation
        """
        if self.__has_conflicting_node_names():  # if the graph has nodes with conflicting node names
            raise Exception("Error: Nodes have conflicting names")  # raise an exception
        if self.__has_incompatible_matrix_dimensions():  # if the matrix dimensions are incompatible
            raise Exception("Error: Nodes list and adjacency matrix have incompatible dimensions")  # raise an exception

