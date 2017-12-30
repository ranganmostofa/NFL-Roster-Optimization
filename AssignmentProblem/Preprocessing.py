from BipartiteGraph import GraphProcessing


class Preprocessing:
    """
    Class that houses static preprocessing methods essential to and shared by the different algorithms
    implemented in this package
    """

    @staticmethod
    def modify_graph(G, matching, update_func):
        """
        Given a BipartiteGraph object, a matching and an update function, invokes the input update function
        using the matched source node, terminal node and edge as inputs
        """
        G_prime = G.__deepcopy__()  # produce a deep copy of the input graph
        for source_node_name, terminal_node_name in matching:  # for every pair of node names in the matching
            # obtain the source and terminal Node objects
            source_node = GraphProcessing.search_node_names(G_prime.get_left_nodeset(), source_node_name).pop()
            terminal_node = GraphProcessing.search_node_names(G_prime.get_right_nodeset(), terminal_node_name).pop()
            for edge in source_node.get_outgoing_edges():  # for every edge originating from the source node
                # if the edge leads to the terminal node
                if terminal_node_name.__eq__(edge.get_terminal_node().get_name()):
                    update_func(source_node, terminal_node, edge)  # invoke the update function
        return G_prime  # return the modified graph

    @staticmethod
    def reverse_matched_directed_edge(source_node, terminal_node, matched_edge):
        """
        Given a source node, a terminal node and the edge connecting them, reverses the direction of the
        edge so that the edge originates from the terminal node and leads to the source node
        """
        # reverse the direction in the source node object
        source_node.remove_outgoing_edge(terminal_node.get_name())
        source_node.add_incoming_edge(matched_edge)

        # reverse the direction in the terminal node object
        terminal_node.remove_incoming_edge(source_node.get_name())
        terminal_node.add_outgoing_edge(matched_edge)

        # reverse the direction in the edge object
        matched_edge.set_source_node(terminal_node)
        matched_edge.set_terminal_node(source_node)

