from Dijkstra import Dijkstra
from AssignmentProblem import AssignmentProblem
from BipartiteGraph import BipartiteGraph, GraphProcessing


class EdmondsKarp:
    """
    Class that implements the Edmonds-Karp Algorithm which aims to solve the maximum weighted matching
    problem on bipartite graphs (O(n^3) runtime complexity)
    """

    LABELING_ATTRIBUTE = "Label"  # initialize global variables

    @staticmethod
    def apply(G):
        """
        Given a BipartiteGraph object, utilizes the Edmonds-Karp algorithm to compute and return a maximum
        weighted matching for the input graph, represented as a set of pairs where each pair consists of
        source node and terminal node names in that order
        """
        G_prime = \
            EdmondsKarp.__create_initial_vertex_labeling(  # create initial vertex labeling
                AssignmentProblem.construct_balanced_equivalent(  # balance the left and right nodesets
                    AssignmentProblem.remove_disconnected_nodes(G)  # remove disconnected nodes
                )
            ).add_node_attributes(AssignmentProblem.MATCHING_ATTRIBUTE, False)\
             .add_edge_attributes(AssignmentProblem.MATCHING_ATTRIBUTE, False)
        # initialize matching attributes for all nodes and edge

        # initialize initial mapping to an empty set
        current_matching = set()
        while not AssignmentProblem.is_perfect(G_prime, current_matching):  # while the matching is not perfect

            # choose an arbitrary exposed vertex - this is the root node of the alternating tree
            root_node = EdmondsKarp.__select_arbitrary_exposed_vertex(G_prime, current_matching)
            # initialize the alternating tree in terms of the source and terminal nodesets
            S, T = {root_node.get_name()}, set()

            # obtain the edge-induced equality subgraph
            G_equality_subgraph = EdmondsKarp.__construct_equality_subgraph(G_prime)
            # compute the joint neighborhood of all source nodes in the alternating tree
            joint_neighborhood = EdmondsKarp.__compute_joint_neighborhood(G_equality_subgraph, S)

            while True:  # enter an infinite loop - termination criteria are explained below

                if not len(T.symmetric_difference(joint_neighborhood)):  # if the joint neighborhood and T are equal
                    # update the labeling of the actual graph, the equality subgraph and the joint neighborhood
                    G_prime = EdmondsKarp.__adjust_labeling(G_prime, S, T)
                    G_equality_subgraph = EdmondsKarp.__construct_equality_subgraph(G_prime)
                    joint_neighborhood = EdmondsKarp.__compute_joint_neighborhood(G_equality_subgraph, S)

                leaf_node = \
                    GraphProcessing.search_node_names(
                        G_equality_subgraph.get_right_nodeset(),
                        joint_neighborhood.difference(T).pop()
                    ).pop()  # if the joint neighborhood and T are not equal, select a leaf node

                # if the selected leaf node is not matched
                if not leaf_node.get_attribute_value(AssignmentProblem.MATCHING_ATTRIBUTE):
                    augmenting_path = \
                        AssignmentProblem.postprocess_augmenting_path(
                            EdmondsKarp.__compute_augmenting_path(
                                G_equality_subgraph,
                                current_matching,
                                root_node,
                                leaf_node
                            )
                        )  # compute an augmenting path from the root node to the leaf node

                    # augment the current matching with the computed path above
                    current_matching = current_matching.symmetric_difference(set(augmenting_path))
                    G_prime = \
                        AssignmentProblem.modify_graph(
                            G_prime,
                            current_matching,
                            AssignmentProblem.update_matched_attributes
                        )  # update the attributes of matched nodes and edges based on the new matching
                    break  # terminate infinite loop

                # if the leaf node is already matched, determine the node it is matched with
                matching_leaf_node_name = \
                    {
                        source_node_name
                        for source_node_name, terminal_node_name in current_matching
                        if terminal_node_name == leaf_node.get_name()
                    }.pop()
                # add the leaf node and its matching counterpart to the alternating tree
                S.add(matching_leaf_node_name), T.add(leaf_node.get_name())

        # apply postprocessing techniques and return the final maximum matching
        return AssignmentProblem.postprocess_maximum_matching(current_matching)

    @staticmethod
    def __create_initial_vertex_labeling(G):
        """
        Given a BipartiteGraph object, returns a modified graph with assigned vertex labels such that the
        constraints are fulfilled, i.e. the labeling is feasible: the sum of the labels of two nodes is
        greater than or equal to the weight of the edge connecting them
        """
        G_prime = G.add_node_attributes(EdmondsKarp.LABELING_ATTRIBUTE, 0)  # initialize all vertex labels to 0

        for edge in G_prime.get_edges():  # for every edge in the graph
            if not EdmondsKarp.__check_labeling_feasibility(edge):  # if the labeling is not yet feasible
                # obtain variables for the source and terminal node objects
                source_node, terminal_node = edge.get_source_node(), edge.get_terminal_node()

                # set the vertex label for all source nodes to the edge weight - eventually the initial vertex
                # label of a source node becomes equal to the maximum of the edge weights of all outgoing edges
                source_node.set_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE, edge.get_weight())

                # set the vertex label for all terminal nodes to 0
                terminal_node.set_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE, 0)

        return G_prime  # return the modified graph with the initial vertex labels

    @staticmethod
    def __check_labeling_feasibility(edge):
        """
        Given an edge, returns True if the sum of the vertex labels of the nodes it connects is greater than
        or equal to the weight of the edge, and False otherwise
        """
        return \
            edge.get_source_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) + \
            edge.get_terminal_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) >= \
            edge.get_weight()  # return whether the vertex labels are feasible

    @staticmethod
    def __construct_equality_subgraph(G):
        """
        Given a BipartiteGraph object, returns a subgraph that contains all nodes in the original graph, but
        only those edges whose weight equals the node labels of the source and terminal nodes it connects
        """
        return \
            BipartiteGraph.extract_edge_induced_subgraph(
                G,
                # include only those edges that connect nodes with labels whose sum equals the
                # weight of the edge
                lambda edge:
                edge.get_source_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) +
                edge.get_terminal_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) ==
                edge.get_weight()
            )  # return the edge-induced subgraph

    @staticmethod
    def __select_arbitrary_exposed_vertex(G, matching):
        """
        Given a BipartiteGraph object and a matching represented as a set of pairs of node names, returns an
        arbitrary exposed vertex from the left nodeset
        """
        if not matching:  # if the matching is empty
            return G.get_left_nodeset().pop()  # return any vertex

        target_nodeset = \
            {
                node  # add the node to the set
                for node in G.get_left_nodeset()  # for every node in the left nodeset
                if node.get_name() not in list(zip(*matching)).pop(0)  # if the node is part of the matching
            }

        if len(target_nodeset):  # if at least one exposed vertex exists
            return target_nodeset.pop()  # return one of the exposed vertices

    @staticmethod
    def __compute_joint_neighborhood(G, nodeset):
        """
        Given a BipartiteGraph object and a nodeset, returns the union of the sets of names of nodes adjacent
        to every node in the input nodeset
        """
        return \
            set(
                {
                    edge.get_terminal_node().get_name()  # obtain the name of the adjacent node
                    for node_name in nodeset  # for every node in the nodeset
                    for edge in GraphProcessing.search_node_names(  # for every edge originating from the node
                        G.get_left_nodeset(),
                        node_name
                    ).pop()
                     .get_outgoing_edges()
                }
            )  # return the set of adjacent node names

    @staticmethod
    def __adjust_labeling(G, S, T):
        """
        Given a BipartiteGraph object and the current alternating tree in terms of the source (S) and terminal
        (T) nodesets, returns a modified graph with the updated vertex labels
        """
        G_prime = G.__deepcopy__()  # create a deepcopy of the input graph

        delta = EdmondsKarp.__compute_delta(G_prime, S, T)  # compute the required change in vertex labels

        for node in G_prime.get_left_nodeset().union(G_prime.get_right_nodeset()):  # for every node in the graph
            current_label = node.get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE)  # obtain the current label
            # if the node is in the left nodeset of the alternating tree, subtract delta
            if node.get_name() in S: node.set_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE, current_label - delta)
            # if the node is in the right nodeset of the alternating tree, add delta
            elif node.get_name() in T: node.set_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE, current_label + delta)

        return G_prime  # return the modified graph

    @staticmethod
    def __compute_delta(G, S, T):
        """
        Given a BipartiteGraph object and the current alternating tree in terms of the source (S) and terminal
        (T) nodesets, computes and returns the magnitude of adjustment required for the vertex labels
        """
        return \
            min(
                {
                    edge.get_source_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) +  # source label
                    edge.get_terminal_node().get_attribute_value(EdmondsKarp.LABELING_ATTRIBUTE) -  # terminal label
                    edge.get_weight()  # edge weight
                    for edge in G.get_edges()  # for every edge
                    # if source node and terminal nodes are present in S and T respectively
                    if edge.get_source_node().get_name() in S and
                       edge.get_terminal_node().get_name() in set(G.get_right_node_names()).difference(T)
                }
            )  # return the minimum across all edges

    @staticmethod
    def __compute_augmenting_path(G, matching, source, sink):
        """
        Given a BipartiteGraph object and a set of pairs of matched nodes, computes and returns the shortest
        available augmenting path if one exists
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

        G_prime_dict = GraphProcessing.bipartite_to_dictionary_form(G_prime)
        dist, prev_node = \
            Dijkstra.one_to_many(
                    G_prime_dict,
                    source.get_name()
            )  # invoke Dijkstra's algorithm to compute the shortest path from the source to the sink node

        augmenting_path = list()  # initialize an empty augmenting path
        current_node = sink.get_name()  # begin traceback from the sink node

        # while the source node has not been reached
        while current_node != source.get_name():
            if current_node not in prev_node.keys():  # if a discontinuity exists
                augmenting_path.clear()  # empty the augmenting path list
                break  # terminate loop
            previous_node = prev_node[current_node]  # obtain the node previous to current node in the shortest path
            # append the edge connecting the previous node to the current node as a pair to the augmenting path
            augmenting_path.append(tuple((previous_node, current_node)))
            current_node = previous_node  # replace the current node with the previous node
        # reverse and return the resulting path
        return tuple(reversed(augmenting_path))

