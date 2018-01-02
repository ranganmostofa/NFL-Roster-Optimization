import random
from sys import maxsize
from BipartiteGraph import Node, BipartiteGraph, GraphProcessing


class AssignmentProblem:
    """
    Class that houses static methods essential to and shared by the different algorithms implemented in
    this package
    """

    DUMMY_EDGE_WEIGHT = 0  # initialize global variables

    DUMMY_NODE_NAME = "Dummy Node"

    MATCHING_ATTRIBUTE = "Matched"

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
    def construct_balanced_equivalent(G):
        """
        Given a BipartiteGraph object, balances the left and right nodesets, i.e. creates dummy nodes and
        edges to ensure the cardinality of the left and right nodesets are equal
        """
        G_prime = G.__deepcopy__()  # create a deep copy of the input graph

        # determine which nodeset is complete and which is deficient
        if len(G_prime.get_left_nodeset()) > len(G_prime.get_right_nodeset()):
            complete_nodeset, deficient_nodeset = G_prime.get_left_nodeset(), G_prime.get_right_nodeset()
        else:
            complete_nodeset, deficient_nodeset = G_prime.get_right_nodeset(), G_prime.get_left_nodeset()

        left_deficiency = len(deficient_nodeset) == len(G_prime.get_left_nodeset())

        while not G_prime.is_balanced():  # while the graph is not balanced
            dummy_node = \
                Node(
                    AssignmentProblem.DUMMY_NODE_NAME + " " + str(random.randint(0, maxsize)),
                    dict(),
                    set(),
                    set()
                )  # create a dummy node

            for node in complete_nodeset:  # for every node in the complete nodeset
                # add the dummy node to the graph and add a dummy edge connecting the dummy node and the node
                # in the complete nodeset
                if left_deficiency: G_prime.add_edge(AssignmentProblem.DUMMY_EDGE_WEIGHT, dict(), dummy_node, node)
                else: G_prime.add_edge(AssignmentProblem.DUMMY_EDGE_WEIGHT, dict(), node, dummy_node)

        return G_prime  # return the balanced graph

    @staticmethod
    def remove_disconnected_nodes(G):
        """
        Given a BipartiteGraph object, returns a graph similar to the input graph but lacking the
        disconnected nodes
        """
        left_nodeset = \
            {
                node
                for node in G.get_left_nodeset()
                if len(node.get_outgoing_edges().union(node.get_incoming_edges()))
            }  # create a new left nodeset by filtering out the disconnected nodes

        right_nodeset = \
            {
                node
                for node in G.get_right_nodeset()
                if len(node.get_outgoing_edges().union(node.get_incoming_edges()))
            }  # create a new right nodeset by filtering out the disconnected nodes

        return BipartiteGraph(left_nodeset, right_nodeset)  # return the modified graph

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

    @staticmethod
    def update_matched_attributes(source_node, terminal_node, edge):
        """
        Given a source node, a terminal node and the edge connecting them, sets the matching attribute
        of all three graph elements to True
        """
        # set the matching attribute to true
        source_node.set_attribute_value(AssignmentProblem.MATCHING_ATTRIBUTE, True)
        terminal_node.set_attribute_value(AssignmentProblem.MATCHING_ATTRIBUTE, True)
        edge.set_attribute_value(AssignmentProblem.MATCHING_ATTRIBUTE, True)

    @staticmethod
    def postprocess_augmenting_path(augmenting_path):
        """
        Given an augmenting path represented as a tuple of pairs where each pair consists of source node
        and terminal node names in that order, undoes the reversal of every odd-indexed edge executed prior
        to computing the augmenting path
        """
        return \
            tuple(
                (
                    tuple(
                        (
                            terminal_node,
                            source_node
                        )  # undo the reversal if the index is odd
                    ) if list(augmenting_path).index(tuple((source_node, terminal_node))) % 2

                    else tuple(
                        (
                            source_node,
                            terminal_node
                        )  # maintain original orientation otherwise
                    )

                    # continue for every pair of source and terminal nodes
                    for source_node, terminal_node in augmenting_path
                )
            )

    @staticmethod
    def postprocess_maximum_matching(maximum_matching):
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
                    if AssignmentProblem.DUMMY_NODE_NAME not in source_node_name and
                       AssignmentProblem.DUMMY_NODE_NAME not in terminal_node_name  # with no dummy nodes
                }
            )  # return the filtered set

