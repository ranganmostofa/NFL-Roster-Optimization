from Dijkstra import Dijkstra
from BipartiteGraph import GraphProcessing
from AssignmentProblem import AssignmentProblem


class MaximumCardinalityMatching:
    """
    Class containing implementation of the maximum cardinality matching algorithm (O(n^3) runtime complexity)
    """

    # initialize global variables

    SOURCE_NODE, SINK_NODE = "Source Node", "Sink Node"

    @staticmethod
    def apply(G, initial_matching):
        """
        Given a BipartiteGraph object and an initial matching, computes and returns a maximum cardinality
        matching for the input graph, represented as a set of pairs where each pair consists of source
        node and terminal node names in that order
        """
        current_matching = initial_matching  # start off with an empty matching
        # operate on a duplicate graph
        G_prime = G\
            .add_node_attributes(AssignmentProblem.MATCHING_ATTRIBUTE, False)\
            .add_edge_attributes(AssignmentProblem.MATCHING_ATTRIBUTE, False)

        while True:  # enter an infinite loop that terminates only when no augmenting paths exist
            augmenting_path = \
                AssignmentProblem.postprocess_augmenting_path(
                    MaximumCardinalityMatching.compute_augmenting_path(
                        G_prime,
                        current_matching
                    )
                )  # compute an augmenting path - the shortest, since Dijkstra's is being used

            if not augmenting_path:  # if no augmenting path exists terminate loop
                break

            # compute the symmetric difference between the current matching and the augmenting path
            current_matching = current_matching.symmetric_difference(set(augmenting_path))
            G_prime = \
                AssignmentProblem.modify_graph(
                    G_prime,
                    current_matching,
                    AssignmentProblem.update_matched_attributes
                )  # update the attributes of matched nodes and edges based on new matching

        return current_matching  # return the matching

    @staticmethod
    def compute_augmenting_path(G, matching):
        """
        Given a BipartiteGraph object and a set of pairs of matched nodes, computes and returns the
        shortest available augmenting path if one exists
        """
        G_prime = \
            AssignmentProblem.modify_graph(
                G,
                matching,
                AssignmentProblem.reverse_matched_directed_edge
            )  # reverse the direction of the edges included in the matching

        # modify all edge weights to be identical
        # allows for a shortest path to be computed based on edge cardinality
        for edge in G_prime.get_edges(): edge.set_weight(AssignmentProblem.DUMMY_EDGE_WEIGHT)

        G_prime_dict = \
            MaximumCardinalityMatching.__add_source_sink_nodes(
                G_prime,
                matching
            )  # attach source and sink nodes to the graph

        dist, prev_node = \
            Dijkstra.one_to_many(
                    G_prime_dict,
                    MaximumCardinalityMatching.SOURCE_NODE,
            )  # invoke Dijkstra's algorithm to compute the shortest path from the source to the sink node

        augmenting_path = list()  # initialize an empty augmenting path
        current_node = MaximumCardinalityMatching.SINK_NODE  # begin traceback from the sink node

        # while the source node has not been reached
        while current_node != MaximumCardinalityMatching.SOURCE_NODE:
            if current_node not in prev_node.keys():  # if a discontinuity exists
                augmenting_path.clear()  # empty the augmenting path list
                break  # terminate loop
            previous_node = prev_node[current_node]  # obtain the node previous to current node in the shortest path
            # append the edge connecting the previous node to the current node as a pair to the augmenting path
            augmenting_path.append(tuple((previous_node, current_node)))
            current_node = previous_node  # replace the current node with the previous node
        # clip off the source and sink nodes and return the resulting path
        return tuple(reversed(augmenting_path[1:len(augmenting_path) - 1]))

    @staticmethod
    def __add_source_sink_nodes(G, matching):
        """
        Given a BipartiteGraph object and a set of pairs of matched nodes, returns a graph with the
        following modifications:

        (1) Converts the graph object to dictionary form
        (2) Adds a source and sink node to the graph
        (3) Connects the source node to every exposed node in the left nodeset
        (4) Connects every exposed node in the right nodeset to the sink node
        """
        G_dict = GraphProcessing.bipartite_to_dictionary_form(G)  # convert to dictionary form

        # obtain the list of matched nodes in the left and right nodesets
        if matching: matched_source_node_names, matched_terminal_node_names = zip(*list(matching))
        else: matched_source_node_names, matched_terminal_node_names = list(), list()

        # add the source and sink nodes
        G_dict[MaximumCardinalityMatching.SOURCE_NODE], G_dict[MaximumCardinalityMatching.SINK_NODE] = dict(), dict()
        for source_node in G.get_left_nodeset():  # for every node in the left nodeset
            if source_node.get_name() not in matched_source_node_names:  # if the node is exposed
                # connect the source node to the exposed node using a dummy edge
                G_dict[
                    MaximumCardinalityMatching.SOURCE_NODE
                ][
                    source_node.get_name()
                ] = \
                    AssignmentProblem.DUMMY_EDGE_WEIGHT

        for terminal_node in G.get_right_nodeset():  # for every node in the right nodeset
            if terminal_node.get_name() not in matched_terminal_node_names:  # if the node is exposed
                # connect the terminal node to the sink node using a dummy edge
                G_dict[
                    terminal_node.get_name()
                ][
                    MaximumCardinalityMatching.SINK_NODE
                ] = \
                    AssignmentProblem.DUMMY_EDGE_WEIGHT

        return G_dict  # return the modified graph in dictionary form

