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
                node for node in nodeset
                if node.get_name().__eq__(target_name)
            }

