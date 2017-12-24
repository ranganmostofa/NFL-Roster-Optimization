from Edge import Edge


class BipartiteGraph:
    """
    General-purpose BipartiteGraph class for the BipartiteGraph module
    """
    def __init__(self, left_nodeset, right_nodeset):
        """
        Constructor for the BipartiteGraph class - used to initialize all necessary fields of the
        BipartiteGraph object
        """
        self.left_nodeset = left_nodeset  # initialize all necessary fields
        self.right_nodeset = right_nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def __str__(self):
        """
        Returns a neatly formatted string representation of the BipartiteGraph object
        """
        # string representation includes values of all inner fields
        return \
            "Left Nodeset: " + str(self.left_nodeset) + "\n" + \
            "Right Nodeset: " + str(self.right_nodeset) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the BipartiteGraph object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given a BipartiteGraph object, checks whether this BipartiteGraph object is equal to the input
        BipartiteGraph object - equality of two BipartiteGraph objects is defined in terms of equality
        of inner fields and not as identical objects in memory
        """
        # check equality of the left and right nodesets
        return \
            self.left_nodeset.__eq__(other.get_left_nodeset()) and \
            self.right_nodeset.__eq__(other.get_right_nodeset())

    def add_left_node(self, node):
        """
        Given a Node object, adds the input to the left nodeset of the bipartite graph
        """
        self.left_nodeset.add(node)  # add the input node to the left nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def add_right_node(self, node):
        """
        Given a Node object, adds the input to the right nodeset of the bipartite graph
        """
        self.right_nodeset.add(node)  # add the input node to the right nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def add_edge(self, weight, attributes, source_node, terminal_node):
        """
        Given the necessary inner fields of an Edge object, creates the Edge object and connects the
        source and terminal nodes using this edge
        """
        if source_node not in self.left_nodeset:  # if the source node is not in the left nodeset
            self.add_left_node(source_node)  # add the source node
        if terminal_node not in self.right_nodeset:  # if the terminal node is not in the right nodeset
            self.add_right_node(terminal_node)  # add the terminal node
        edge = Edge(weight, attributes, source_node, terminal_node)  # create the Edge object
        source_node.add_outgoing_edge(edge)  # connect the source node and the terminal node using the edge
        terminal_node.add_incoming_edge(edge)

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def get_left_nodeset(self):
        """
        Returns the left nodeset of the bipartite graph
        """
        return self.left_nodeset  # return the left nodeset

    def get_right_nodeset(self):
        """
        Returns the right nodeset of the bipartite graph
        """
        return self.right_nodeset  # return the right nodeset

    def get_edges(self):
        """
        Returns a set of the edges in the bipartite graph
        """
        return set(
                [edge for node in self.left_nodeset for edge in node.get_outgoing_edges()] +
                [edge for node in self.left_nodeset for edge in node.get_incoming_edges()]
        )

    def set_left_nodeset(self, left_nodeset):
        """
        Given a set of nodes, sets the input as the current left nodeset
        """
        self.left_nodeset = left_nodeset  # overwrite the existing left nodeset with the input left nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def set_right_nodeset(self, right_nodeset):
        """
        Given a set of nodes, sets the input as the current right nodeset
        """
        self.right_nodeset = right_nodeset  # overwrite the existing right nodeset with the input right nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def __is_bipartite(self):
        """
        Returns true if the graph is bipartite and false otherwise
        """
        # check if overlap exists between the two nodesets
        if len(self.left_nodeset.intersection(self.right_nodeset)) > 0:
            return False  # if so, the graph is not bipartite

        for node in self.left_nodeset:  # for every node in the left nodeset
            for edge in node.get_outgoing_edges():  # for every outgoing edge
                # if the edge originates from the right nodeset or terminates at the left nodeset
                if edge.get_source_node() in self.right_nodeset or edge.get_terminal_node() in self.left_nodeset:
                    return False  # the graph is not bipartite

            for edge in node.get_incoming_edges():  # for every incoming edge
                # if the edge originates from the left nodeset or terminates at the right nodeset
                if edge.get_source_node() in self.left_nodeset or edge.get_terminal_node() in self.right_nodeset:
                    return False  # the graph is not bipartite

        for node in self.right_nodeset:  # for every node in the right nodeset
            for edge in node.get_incoming_edges():  # for every incoming edge
                # if the edge originates from the right nodeset or terminates at the left nodeset
                if edge.get_source_node() in self.right_nodeset or edge.get_terminal_node() in self.left_nodeset:
                    return False  # the graph is not bipartite

            for edge in node.get_outgoing_edges():  # for every outgoing edge
                # if the edge originates from the left nodeset or terminates at the right nodeset
                if edge.get_source_node() in self.left_nodeset or edge.get_terminal_node() in self.right_nodeset:
                    return False  # the graph is not bipartite

        return True  # if all the tests above have passed, the graph must be bipartite

    def __check_validity(self):
        """
        Throws an exception if the graph is not bipartite - called after every mutation
        """
        if not self.__is_bipartite():  # if the graph is not bipartite
            raise Exception("Error: Graph is not bipartite")  # raise an exception

