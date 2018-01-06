from Edge import Edge
from GraphProcessing import GraphProcessing


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
            "Left Nodeset: " + "\n".join([node.__str__() for node in self.left_nodeset]) + "\n" + \
            "Right Nodeset: " + "\n".join([node.__str__() for node in self.right_nodeset]) + "\n"

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

    def __deepcopy__(self):
        """
        Creates and returns a deepcopy of the current BipartiteGraph object - all internal nodes
        and edges and their respective internal fields are replicated without invoking an infinite
        recursive call
        """
        return BipartiteGraph.extract_edge_induced_subgraph(self, lambda edge: True)  # copy all edges

    def add_node_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of the nodes in the left and right nodesets of the graph
        """
        G_prime = self.__deepcopy__()  # create a deepcopy of the bipartite graph
        for node in G_prime.get_left_nodeset().union(G_prime.get_right_nodeset()):  # for every node in the graph
            # add the attribute key-value pair to the attributes registry of the node
            node.add_attribute(attribute_key, attribute_value)
        return G_prime  # return the modified graph

    def add_edge_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of the edges in the graph
        """
        G_prime = self.__deepcopy__()  # create a deepcopy of the bipartite graph
        for edge in G_prime.get_edges():  # for every edge in the graph
            # add the attribute key-value pair to the attributes registry of the edge
            edge.add_attribute(attribute_key, attribute_value)
        return G_prime  # return the modified graph

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
        # if the source node is not in the left nodeset
        if source_node.get_name() not in self.get_left_node_names():
            self.add_left_node(source_node)  # add the source node

        # if the terminal node is not in the right nodeset
        if terminal_node.get_name() not in self.get_right_node_names():
            self.add_right_node(terminal_node)  # add the terminal node

        edge = Edge(weight, attributes, source_node, terminal_node)  # create the Edge object
        source_node.add_outgoing_edge(edge)  # connect the source node and the terminal node using the edge
        terminal_node.add_incoming_edge(edge)

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def get_left_nodeset(self):
        """
        Returns the left nodeset of the bipartite graph
        """
        return set(self.left_nodeset)  # return the left nodeset

    def get_left_node_names(self):
        """
        Returns a set of names belonging to the nodes in the left nodeset of the bipartite graph
        """
        return set({node.get_name() for node in self.get_left_nodeset()})  # return the set of names

    def get_right_nodeset(self):
        """
        Returns the right nodeset of the bipartite graph
        """
        return set(self.right_nodeset)  # return the right nodeset

    def get_right_node_names(self):
        """
        Returns a set of names belonging to the nodes in the right nodeset of the bipartite graph
        """
        return set({node.get_name() for node in self.get_right_nodeset()})  # return the set of names

    def get_edges(self):
        """
        Returns a list of the edges in the bipartite graph
        """
        return \
            [edge for node in self.left_nodeset for edge in node.get_outgoing_edges()] + \
            [edge for node in self.left_nodeset for edge in node.get_incoming_edges()]

    def set_left_nodeset(self, left_nodeset):
        """
        Given a set of nodes, sets the current left nodeset as the input
        """
        self.left_nodeset = set(left_nodeset)  # overwrite the existing left nodeset with the input left nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    def set_right_nodeset(self, right_nodeset):
        """
        Given a set of nodes, sets the current right nodeset as the input
        """
        self.right_nodeset = set(right_nodeset)  # overwrite the existing right nodeset with the input right nodeset

        self.__check_validity()  # check if graph is bipartite - throws exception if not

    @staticmethod
    def extract_edge_induced_subgraph(G, predicate):
        """
        Given a BipartiteGraph object and a predicate that accepts Edge objects as inputs, returns the
        edge-induced subgraph of the input graph based on the set of edges filtered by the input predicate.

        NOTE: An edge-induced subgraph is defined here as a graph with a set of nodes exactly identical to
              the original set but with the filtered set of edges. As a result, the subgraph may contain
              disconnected nodes. However, as an added bonus of using this convention, this method may
              also be used to efficiently produce deep copies of an existing graph
        """
        # initialize the new left and right nodesets as sets containing disconnected copies of the original nodes
        left_nodeset, right_nodeset = \
            {GraphProcessing.produce_duplicate_disconnected_node(node) for node in G.get_left_nodeset()}, \
            {GraphProcessing.produce_duplicate_disconnected_node(node) for node in G.get_right_nodeset()}

        # for every original source node
        for original_source_node in G.get_left_nodeset().union(G.get_right_nodeset()):
            # access the corresponding copy source node using the unique name ID
            copy_source_node = \
                GraphProcessing.search_node_names(
                    set(left_nodeset.union(right_nodeset)),
                    original_source_node.get_name()
                ).pop()

            # for every original edge leading from the current original source node
            for original_edge in original_source_node.get_outgoing_edges():
                if predicate(original_edge):
                    # access the corresponding copy terminal node using the unique name ID
                    copy_terminal_node = \
                        GraphProcessing.search_node_names(
                            set(left_nodeset.union(right_nodeset)),
                            original_edge.get_terminal_node().get_name()
                        ).pop()

                    # create the copy edge using the copy source and terminal nodes
                    copy_edge = \
                        Edge(
                            original_edge.get_weight(),
                            dict(original_edge.get_attributes()),
                            copy_source_node,
                            copy_terminal_node
                        )

                    # add the edge to the copy source and terminal nodes
                    copy_source_node.add_outgoing_edge(copy_edge)
                    copy_terminal_node.add_incoming_edge(copy_edge)

        # finally, return the deepcopy version of the current BipartiteGraph object
        return BipartiteGraph(left_nodeset, right_nodeset)

    def is_balanced(self):
        """
        Returns True if the bipartite graph is balanced i.e. the cardinality of the left nodeset is equal
        to that of the right nodeset and False otherwise
        """
        # return if the left and right nodesets are of equal size
        return len(self.left_nodeset) == len(self.right_nodeset)

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

    def __has_conflicting_node_names(self):
        """
        Returns True if the graph nodes have conflicting names and False otherwise
        """
        # check length of sets to determine if overlap exists
        return \
            len({node.get_name() for node in self.get_left_nodeset().union(self.get_right_nodeset())}) \
            != len(self.get_left_nodeset()) + len(self.get_right_nodeset())

    def __has_multiple_edges(self):
        """
        Returns True if the graph has multiple edges originating from and leading to the same node and False
        otherwise
        """
        return \
            len(
                list(
                    [
                        tuple((edge.get_source_node().get_name(), edge.get_terminal_node().get_name()))
                        for edge in self.get_edges()
                    ]  # the length of the list which allows duplicates...
                )
            ) != \
            len(
                set(
                    {
                        tuple((edge.get_source_node().get_name(), edge.get_terminal_node().get_name()))
                        for edge in self.get_edges()
                    }  # ...should equal the length of the set that does not allow duplicates
                )
            )  # return True if the two data structures are equal in size and False otherwise

    def __check_validity(self):
        """
        Throws an exception if:

        (1) Graph is not bipartite
        (2) Nodes have conflicting names
        (3) Multiple edges exist

        Method should be called after every mutation
        """
        if not self.__is_bipartite():  # if the graph is not bipartite
            raise Exception("Error: Graph is not bipartite")  # raise an exception
        if self.__has_conflicting_node_names():  # if the graph has nodes with conflicting node names
            raise Exception("Error: Nodes have conflicting names")  # raise an exception
        if self.__has_multiple_edges():  # if the graph has nodes with multiple edges
            raise Exception("Error: Multiple edges exist")  # raise an exception

