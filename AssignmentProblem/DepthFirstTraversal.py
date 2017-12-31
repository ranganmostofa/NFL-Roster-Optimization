from BipartiteGraph import GraphProcessing


class DepthFirstTraversal:
    """
    Class that houses implementation of the depth-first search algorithm (O(m + n) runtime complexity)
    """

    VISITED_ATTRIBUTE = "Visited"  # initialize global variables

    @staticmethod
    def apply(G, initial_node):
        """
        Given a BipartiteGraph object and an initial node, performs depth-first search on the graph,
        starting from the initial node and returns a graph with nodes that have a "visited" boolean
        attribute to indicate whether the node was visited during the search
        """
        # initialize the "visited" attribute for each node
        G_prime = G.add_node_attributes(DepthFirstTraversal.VISITED_ATTRIBUTE, False)
        DepthFirstTraversal.__depth_first_search_recursive_helper(
            GraphProcessing.search_node_names(
                G_prime.get_left_nodeset().union(G_prime.get_right_nodeset()), initial_node.get_name()
            ).pop()
        )  # perform depth-first search
        return G_prime  # return the graph with nodes that include the "visited" attribute

    @staticmethod
    def __depth_first_search_recursive_helper(initial_node):
        """
        Given the initial Node object, performs depth-first search traversal on the graph containing
        the input node using recursion
        """
        # set the initial node as visited
        initial_node.set_attribute_value(DepthFirstTraversal.VISITED_ATTRIBUTE, True)
        for edge in initial_node.get_outgoing_edges():  # for every edge originating from the initial node
            neighbor = edge.get_terminal_node()  # obtain the neighbor Node object
            # if the neighbor has not been visited yet
            if not neighbor.get_attribute_value(DepthFirstTraversal.VISITED_ATTRIBUTE):
                # perform a recursive depth-first search using the neighbor as the initial node
                DepthFirstTraversal.__depth_first_search_recursive_helper(neighbor)

