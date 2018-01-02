from AssignmentProblem import AssignmentProblem
from DepthFirstTraversal import DepthFirstTraversal


class MinimumVertexCover:
    """
    Class containing implementation of algorithm which utilizes Konig's Theorem to determine a solution
    to the minimum vertex cover problem (O(n^3) runtime complexity)
    """

    @staticmethod
    def apply(G, maximum_matching):
        """
        Given a BipartiteGraph object and a set of maximum matching, utilizes Konig's Theorem to compute
        and return a minimum vertex cover
        """
        L = set()  # initialize an empty set

        # reverse the direction of the edges that constitute the input maximum matching
        G_prime = AssignmentProblem.modify_graph(G, maximum_matching, AssignmentProblem.reverse_matched_directed_edge)

        # obtain the list of matched nodes in the left nodeset
        matched_left_node_names = {left_node_name for left_node_name, right_node_name in maximum_matching}

        for node in G_prime.get_left_nodeset():  # for every node in the left nodeset
            if node.get_name() not in matched_left_node_names:  # if the node is exposed/unmatched
                # perform depth-first traversal on the input graph
                G_traversed = DepthFirstTraversal.apply(G_prime, node)
                L = MinimumVertexCover.__update_L(G_traversed, L)  # update the set, L, based on the visited nodes

        # assuming A = left node set, B = right node set
        return \
            (
                {
                    node.get_name()
                    for node in G.get_left_nodeset()
                }.difference(L)  # A \ L ...
            ).union(  # (A \ L) union ...
                {
                    node.get_name()
                    for node in G.get_right_nodeset()
                }.intersection(L)  # (A \ L) union (B intersection L)
            )

    @staticmethod
    def __update_L(G, L):
        """
        Given a BipartiteGraph object and a set of node names, updates and returns a modified set that
        includes node names from the input graph that were traversable via depth first search, in addition
        to the original node names in the input set
        """
        return \
            set(L).union(
                {
                    node.get_name()  # add the names of visited nodes
                    for node in G.get_left_nodeset().union(G.get_right_nodeset())
                    if node.get_attribute_value(DepthFirstTraversal.VISITED_ATTRIBUTE)
                }
            )

