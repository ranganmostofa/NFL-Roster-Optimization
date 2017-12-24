class Node:
    """
    General-purpose Node class for the BipartiteGraph module
    """
    def __init__(self, name, attributes, outgoing_edges=list(), incoming_edges=list()):
        """
        Constructor for the Node class - used to initialize all necessary fields of the Node object
        """
        self.name = name  # initialize all necessary fields
        self.attributes = attributes
        self.outgoing_edges = outgoing_edges
        self.incoming_edges = incoming_edges

    def equals(self, node):
        """
        Given a Node object, checks whether this node object is equal to the input node object - equality
        of two node objects is defined in terms of equality of inner fields and not as identical objects
        in memory
        """
        # check equality of names and attributes as well as that of the individual edge objects
        return self.name == node.get_name() and self.attributes == node.get_attributes() and \
               sum([self.outgoing_edges[index].equals(node.get_outgoing_edges()[index])
                    for index in range(len(self.outgoing_edges))]) == len(self.outgoing_edges) and \
               sum([self.incoming_edges[index].equals(node.get_incoming_edges()[index])
                    for index in range(len(self.incoming_edges))]) == len(self.incoming_edges)

    def add_attribute(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of the node
        """
        self.set_attribute_value(attribute_key, attribute_value)  # record the input key-value pair

    def add_outgoing_edge(self, outgoing_edge):
        """
        Given an edge object as input, adds the edge to the existing list of outgoing edges
        """
        self.outgoing_edges.append(outgoing_edge)  # append the input edge to the list of outgoing edges

    def add_incoming_edge(self, incoming_edge):
        """
        Given an edge object as input, adds the edge to the existing list of incoming edges
        """
        self.incoming_edges.append(incoming_edge)  # append the input edge to the list of incoming edges

    def remove_attribute(self, attribute_key):
        """
        Given an attribute key, removes the key-value pair from the attributes registry of the node
        """
        self.attributes.__delitem__(attribute_key)  # delete the input key-value pair

    def remove_outgoing_edge(self, outgoing_edge):
        """
        Given an edge object as input, removes the edge from the existing list of outgoing edges
        """
        # delete the input edge from the list of outgoing edges
        self.set_outgoing_edges(list([edge for edge in self.outgoing_edges if not edge.equals(outgoing_edge)]))

    def remove_incoming_edge(self, incoming_edge):
        """
        Given an edge object as input, removes the edge from the existing list of incoming edges
        """
        # delete the input edge from the list of incoming edges
        self.set_incoming_edges(list([edge for edge in self.incoming_edges if not edge.equals(incoming_edge)]))

    def get_name(self):
        """
        Returns the name of the node
        """
        return self.name  # return the name

    def get_attributes(self):
        """
        Returns the attributes of the node
        """
        return self.attributes  # return the attributes

    def get_attribute_value(self, attribute_key):
        """
        Given an attribute key, accesses and returns the corresponding attribute value
        """
        return self.attributes[attribute_key]  # return the attribute value

    def get_outgoing_edges(self):
        """
        Returns the list of outgoing edges of the node
        """
        return self.outgoing_edges  # return the list of outgoing edges

    def get_incoming_edges(self):
        """
        Returns the list of incoming edges of the node
        """
        return self.incoming_edges  # return the list of incoming edges

    def set_name(self, name):
        """
        Given a name, sets the input as the current name of the node
        """
        self.name = name  # overwrite the existing name with the input name

    def set_attributes(self, attributes):
        """
        Given a registry of attributes, sets the input as the registry of current attributes of the node
        """
        self.attributes = attributes  # overwrite the existing registry of attributes with the input attributes

    def set_attribute_value(self, attribute_key, attribute_value):
        """
        Given an attribute key-value pair, adds the pair to the registry. If an identical attribute key
        exists, the corresponding attribute value is overwritten with the input value
        """
        self.attributes[attribute_key] = attribute_value  # adds the input key-value pair to the registry

    def set_outgoing_edges(self, outgoing_edges):
        """
        Given a list of outgoing edges, sets the input as the current list of outgoing edges
        """
        self.outgoing_edges = outgoing_edges  # overwrite the existing list of outgoing edges with the input list

    def set_incoming_edges(self, incoming_edges):
        """
        Given a list of incoming edges, sets the input as the current list of incoming edges
        """
        self.incoming_edges = incoming_edges  # overwrite the existing list of incoming edges with the input list

