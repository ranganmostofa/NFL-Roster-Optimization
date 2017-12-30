from Node import Node


class GraphProcessing:
    """
    Class that houses static methods related to various graph processing algorithms
    """

    @staticmethod
    def has_attribute_key(graph_element, attribute_key):
        """
        Given a graph element and an attribute key, returns True if the graph element has an attribute
        field of input key and False otherwise
        """
        return attribute_key in graph_element.get_attributes().keys()  # return whether key is present

    @staticmethod
    def has_attribute_value(graph_element, attribute_key, attribute_value):
        """
        Given a graph element and an attribute key-value pair, returns True if the Node object possesses
        the input key-value pair and False otherwise
        """
        # return whether the pair is present
        return graph_element.get_attributes()[attribute_key] == attribute_value

    @staticmethod
    def search_graph_elements(graph_element_set, attribute_key, attribute_value):
        """
        Given a set of graph elements and an attribute key-value pair, returns a filtered set of graph
        elements that possess the input key-value pair
        """
        # return the filtered set of graph elements
        return \
            {
                graph_element for graph_element in graph_element_set
                if GraphProcessing.has_attribute_value(graph_element, attribute_key, attribute_value)
            }

    @staticmethod
    def search_node_names(nodeset, target_name):
        """
        Given a set of nodes, returns a filtered set of nodes that have names identical to the input name
        """
        # return the filtered set of nodes
        return \
            {
                node for node in set(nodeset)
                if node.get_name().__eq__(target_name)
            }

    @staticmethod
    def produce_duplicate_disconnected_node(node):
        """
        Given a Node object, returns a disconnected duplicate of the input node
        """
        # retain the original name and attributes, but clear all outgoing and incoming edges
        return \
            Node(
                node.get_name(),
                dict(node.get_attributes()),
                set(),
                set()
            )

    @staticmethod
    def bipartite_to_dictionary_form(G):
        """
        Given a BipartiteGraph object, returns an adjacency matrix representation of the input graph using
        doubly nested dictionaries
        """
        G_dict = dict()  # initialize the adjacency matrix
        for source_node in G.get_left_nodeset().union(G.get_right_nodeset()):  # for every source node
            G_dict[source_node.get_name()] = dict()  # initialize the inner dictionary
            for outgoing_edge in source_node.get_outgoing_edges():  # for every outgoing edge
                terminal_node = outgoing_edge.get_terminal_node()  # obtain the terminal node
                # check the existence of multiple edges and raise an assertion error accordingly
                assert terminal_node.get_name() not in G_dict[source_node.get_name()].keys()
                # add the edge, including the edge weight
                G_dict[source_node.get_name()][terminal_node.get_name()] = outgoing_edge.get_weight()
        return G_dict  # return the populated adjacency matrix representation

