import random
from sys import maxsize
from BipartiteGraph import Node, BipartiteGraph, GraphProcessing


class Preprocessing:
    """
    Class that houses static preprocessing methods essential to and shared by the different algorithms
    implemented in this package
    """

    DUMMY_EDGE_WEIGHT = 0
    DUMMY_NODE_NAME = "Dummy Node"

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
                    Preprocessing.DUMMY_NODE_NAME + " " + str(random.randint(0, maxsize)),
                    dict(),
                    set(),
                    set()
                )  # create a dummy node

            for node in complete_nodeset:  # for every node in the complete nodeset
                # add the dummy node to the graph and add a dummy edge connecting the dummy node and the node
                # in the complete nodeset
                if left_deficiency: G_prime.add_edge(Preprocessing.DUMMY_EDGE_WEIGHT, dict(), dummy_node, node)
                else: G_prime.add_edge(Preprocessing.DUMMY_EDGE_WEIGHT, dict(), node, dummy_node)

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

