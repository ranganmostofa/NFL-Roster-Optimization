from Preprocessing import Preprocessing
from BipartiteGraph import BipartiteGraph
from MinimumVertexCover import MinimumVertexCover
from MaximumCardinalityMatching import MaximumCardinalityMatching


class KuhnMunkres:
    """
    Class that implements the Kuhn-Munkres Algorithm which aims to solve the minimum weighted matching
    problem on bipartite graphs (O(n^4) runtime complexity)
    """

    @staticmethod
    def apply(G):
        """
        Given a BipartiteGraph object, utilizes the Kuhn-Munkres algorithm to compute and return a minimum
        weighted matching for the input graph, represented as a set of pairs where each pair consists of
        source node and terminal node names in that order
        """
        G_prime = \
            KuhnMunkres.__preprocess_weights(  # preprocess the edge weights
                Preprocessing.construct_balanced_equivalent(  # balance the left and right nodesets
                    Preprocessing.remove_disconnected_nodes(G)  # remove disconnected nodes
                )
            )

        maximum_matching = set()  # start with an empty matching
        while True:  # enter an infinite loop - see below for termination criteria
            # extract the subgraph induced by edges with zero-valued weights
            G0_subgraph = KuhnMunkres.__extract_zero_weight_subgraph(G_prime)
            # compute the maximum cardinality matching for the subgraph induced by the zero-weight edges
            # NOTE: The maximum matching from the previous iteration is used as the starting point every time
            #       to reduce the runtime complexity from O(n^5) to O(n^4)
            maximum_matching = set(MaximumCardinalityMatching.apply(G0_subgraph, maximum_matching))
            if KuhnMunkres.is_perfect(G_prime, maximum_matching):  # if the maximum matching is perfect
                break  # terminate the infinite loop
            # otherwise compute the minimum vertex cover for the subgraph induced by the zero-weight edges
            minimum_vertex_cover = set(MinimumVertexCover.apply(G0_subgraph, maximum_matching))
            # adjust the weights of the edges based on the nodes in the minimum vertex cover
            G_prime = KuhnMunkres.__adjust_weights(G_prime, minimum_vertex_cover)

        # apply postprocessing techniques and return the final maximum matching
        return KuhnMunkres.__postprocess_maximum_matching(maximum_matching)

    @staticmethod
    def __preprocess_weights(G):
        """
        Given a BipartiteGraph object, returns a modified graph where the edge weights have been adjusted
        by subtracting the minimum of edge weights of all edges incident to every node in the input graph

        NOTE: This preprocessing step is not absolutely necessary but it decreases the number of main cycle
              iterations of the Kuhn-Munkres algorithm
        """
        G_prime = G.__deepcopy__()  # create a deep copy of the input graph

        for node in G_prime.get_left_nodeset():  # for every node in the left nodeset
            if len(node.get_outgoing_edges()):  # if the node has outgoing edges
                KuhnMunkres.__linear_translation(
                    node.get_outgoing_edges(),
                    min({edge.get_weight() for edge in node.get_outgoing_edges()})
                )  # subtract the minimum of the weights of all outgoing edges from the edge weights

        for node in G_prime.get_right_nodeset():  # for every node in the right nodeset
            if len(node.get_incoming_edges()):  # if the node has incoming edges
                KuhnMunkres.__linear_translation(
                    node.get_incoming_edges(),
                    min({edge.get_weight() for edge in node.get_incoming_edges()})
                )  # subtract the minimum of the weights of all outgoing edges from the edge weights

        return G_prime  # return the preprocessed graph

    @staticmethod
    def __linear_translation(edge_set, value):
        """
        Given a set of Edge objects and a value, subtract the value from the edge weights of all edges in
        the input set
        """
        for edge in edge_set:  # for every edge in the input set
            edge.set_weight(edge.get_weight() - value)  # shift the weight to the left by "value" units

    @staticmethod
    def __extract_zero_weight_subgraph(G):
        """
        Given a BipartiteGraph object, returns the subgraph of the input graph induced by the zero-weight
        edges
        """
        # return the edge induced subgraph based on the zero-weight edges
        return BipartiteGraph.extract_edge_induced_subgraph(G, lambda edge: edge.get_weight() == 0)

    @staticmethod
    def is_perfect(G, maximum_matching):
        """
        Given a BipartiteGraph object and a maximum matching represented as a set of pairs of node names,
        returns True if the input matching is perfect
        """
        G_prime = \
            BipartiteGraph.extract_edge_induced_subgraph(
                G,
                lambda edge: tuple((edge.get_source_node().get_name(),
                                    edge.get_terminal_node().get_name())) in maximum_matching
            )  # extract the edge-induced subgraph based on the matched edges only

        # determine whether every vertex of the graph is incident to exactly one edge of the matching
        return \
            sum(
                [
                    True if len(node.get_outgoing_edges().union(node.get_incoming_edges())) == 1
                    else False
                    for node in G_prime.get_left_nodeset().union(G_prime.get_right_nodeset())
                ]  # number of nodes with a single incident edge...
            ) == len(
                G_prime.get_left_nodeset().union(G_prime.get_right_nodeset())
            )  # ...should equal the total number of nodes

    @staticmethod
    def __adjust_weights(G, minimum_vertex_cover):
        """
        Given a BipartiteGraph object and a minimum vertex cover represented as a set of node names,
        modifies the edge weights in the subgraph to allow for the next iteration in the Kuhn-Munkres
        algorithm
        """
        G_prime = G.__deepcopy__()  # create a deep copy of the graph

        delta = \
            min(
                {
                    edge.get_weight()
                    for edge in G_prime.get_edges()
                    if edge.get_source_node().get_name() not in minimum_vertex_cover and
                       edge.get_terminal_node().get_name() not in minimum_vertex_cover
                }
            )  # compute delta according to the Kuhn-Munkres algorithm

        for edge in G_prime.get_edges():  # for every edge in the graph
            # obtain the source and terminal node names
            source_node_name, terminal_node_name = \
                edge.get_source_node().get_name(), edge.get_terminal_node().get_name()
            # adjust the weights based on the Kuhn-Munkres algorithm
            # if the incident nodes are both in the minimum vertex cover
            if source_node_name in minimum_vertex_cover and terminal_node_name in minimum_vertex_cover:
                edge.set_weight(edge.get_weight() + delta)  # add delta to the edge weight
            # if the incident nodes are both not in the minimum vertex cover
            elif source_node_name not in minimum_vertex_cover and terminal_node_name not in minimum_vertex_cover:
                edge.set_weight(edge.get_weight() - delta)  # subtract delta from the edge weight

        return G_prime  # return the modified graph

    @staticmethod
    def __postprocess_maximum_matching(maximum_matching):
        """
        Given a maximum matching, represented by a set of pairs of node names, removes edges originating
        from or leading to dummy nodes that were introduced in the preprocessing phase to balance the
        bipartite graph
        """
        return \
            set(
                {
                    tuple((source_node_name, terminal_node_name))  # add an edge/pair
                    for source_node_name, terminal_node_name in maximum_matching
                    if Preprocessing.DUMMY_NODE_NAME not in source_node_name and
                       Preprocessing.DUMMY_NODE_NAME not in terminal_node_name  # with no dummy nodes
                }
            )  # return the filtered set

