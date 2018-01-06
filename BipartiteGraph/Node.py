class Node:
    """
    General-purpose Node class for the BipartiteGraph module
    """
    def __init__(self, name, attributes, outgoing_edges, incoming_edges):
        """
        Constructor for the Node class - used to initialize all necessary fields of the Node object

        NOTE: The name field must be unique across all nodes and the attributes dictionary must not
        contain any object references
        """
        self.name = name  # initialize all necessary fields
        self.attributes = attributes
        self.outgoing_edges = outgoing_edges
        self.incoming_edges = incoming_edges

    def __str__(self):
        """
        Returns a neatly formatted string representation of the Node object
        """
        # string representation includes values of all inner fields
        return \
            "Node Name: " + str(self.name) + "\n" + \
            "Node Attributes: " + str(self.attributes) + "\n" + \
            "Outgoing Edges: " + "\n".join([edge.__str__() for edge in self.outgoing_edges]) + "\n" + \
            "Incoming Edges: " + "\n".join([edge.__str__() for edge in self.incoming_edges]) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the Node object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given a Node object, checks whether this Node object is equal to the input Node object - equality
        of two Node objects is defined in terms of equality of their names and not as identical objects
        in memory
        """
        # check equality of names since names are unique identifiers of nodes
        return self.name.__eq__(other.get_name())

    def add_attribute(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of the node
        """
        self.set_attribute_value(attribute_key, attribute_value)  # record the input key-value pair

    def add_outgoing_edge(self, outgoing_edge):
        """
        Given an Edge object as input, adds the edge to the existing set of outgoing edges
        """
        self.outgoing_edges.add(outgoing_edge)  # append the input edge to the set of outgoing edges

    def add_incoming_edge(self, incoming_edge):
        """
        Given an Edge object as input, adds the edge to the existing set of incoming edges
        """
        self.incoming_edges.add(incoming_edge)  # append the input edge to the set of incoming edges

    def remove_attribute(self, attribute_key):
        """
        Given an attribute key, removes the key-value pair from the attributes registry of the node
        """
        self.attributes.__delitem__(attribute_key)  # delete the input key-value pair

    def remove_outgoing_edge(self, terminal_node_name):
        """
        Given the name of an adjacent node, removes the edge leading to the input node, from the
        existing set of outgoing edges
        """
        # delete the input edge from the set of outgoing edges
        self.set_outgoing_edges(
            set(
                [
                    edge
                    for edge in self.outgoing_edges
                    if not edge.get_terminal_node().get_name().__eq__(terminal_node_name)
                ]
            )
        )

    def remove_incoming_edge(self, source_node_name):
        """
        Given the name of an adjacent node, removes the edge originating from the input node, from the
        existing set of outgoing edges
        """
        # delete the input edge from the set of incoming edges
        self.set_incoming_edges(
            set(
                [
                    edge
                    for edge in self.incoming_edges
                    if not edge.get_source_node().get_name().__eq__(source_node_name)
                ]
            )
        )

    def get_name(self):
        """
        Returns the name of the node
        """
        return self.name  # return the name

    def get_attributes(self):
        """
        Returns the attributes of the node
        """
        return dict(self.attributes)  # return the attributes

    def get_attribute_value(self, attribute_key):
        """
        Given an attribute key, accesses and returns the corresponding attribute value
        """
        return self.attributes[attribute_key]  # return the attribute value

    def get_outgoing_edges(self):
        """
        Returns the set of outgoing edges of the node
        """
        return set(self.outgoing_edges)  # return the set of outgoing edges

    def get_incoming_edges(self):
        """
        Returns the set of incoming edges of the node
        """
        return set(self.incoming_edges)  # return the set of incoming edges

    def set_name(self, name):
        """
        Given a name, sets the current name of the node as the input
        """
        self.name = name  # overwrite the existing name with the input name

    def set_attributes(self, attributes):
        """
        Given a registry of attributes, sets the registry of current attributes of the node as the input
        """
        self.attributes = dict(attributes)  # overwrite the existing registry of attributes with the input attributes

    def set_attribute_value(self, attribute_key, attribute_value):
        """
        Given an attribute key-value pair, adds the pair to the registry. If an identical attribute key
        exists, the corresponding attribute value is overwritten with the input value
        """
        self.attributes[attribute_key] = attribute_value  # adds the input key-value pair to the registry

    def set_outgoing_edges(self, outgoing_edges):
        """
        Given a set of outgoing edges, sets the current set of outgoing edges as the input
        """
        self.outgoing_edges = set(outgoing_edges)  # overwrite the existing set of outgoing edges with the input set

    def set_incoming_edges(self, incoming_edges):
        """
        Given a set of incoming edges, sets the current set of incoming edges as the input
        """
        self.incoming_edges = set(incoming_edges)  # overwrite the existing set of incoming edges with the input set

