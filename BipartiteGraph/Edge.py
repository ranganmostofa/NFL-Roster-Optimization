class Edge:
    """
    General-purpose Edge class for the BipartiteGraph module
    """
    def __init__(self, weight, attributes, source_node, terminal_node):
        """
        Constructor for the Edge class - used to initialize all necessary fields of the Edge object
        """
        self.weight = weight  # initialize all necessary fields
        self.attributes = attributes
        self.source_node = source_node
        self.terminal_node = terminal_node

    def __str__(self):
        """
        Returns a neatly formatted string representation of the Edge object
        """
        # string representation includes values of all inner fields
        return \
            "Edge Weight: " + str(self.weight) + "\n" + \
            "Edge Attributes: " + str(self.attributes) + "\n" + \
            "Source Node: \n" + str(self.source_node) + "\n" + \
            "Terminal Node: \n" + str(self.terminal_node) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the Edge object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given an Edge object, checks whether this Edge object is equal to the input Edge object - equality
        of two Edge objects is defined in terms of equality of inner fields and not as identical objects
        in memory
        """
        # check equality of names and attributes as well as that of the individual source and terminal Node objects
        return \
            self.weight == other.get_weight() and \
            self.attributes.__eq__(other.get_attributes()) and \
            self.source_node.__eq__(other.get_source_node()) and \
            self.terminal_node.__eq__(other.get_terminal_node())

    def add_attribute(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of the edge
        """
        self.set_attribute_value(attribute_key, attribute_value)  # record the input key-value pair

    def remove_attribute(self, attribute_key):
        """
        Given an attribute key, removes the key-value pair from the attributes registry of the edge
        """
        self.attributes.__delitem__(attribute_key)  # delete the input key-value pair

    def get_weight(self):
        """
        Returns the weight value of the edge
        """
        return self.weight  # return the weight value

    def get_attributes(self):
        """
        Returns the attributes of the edge
        """
        return self.attributes  # return the attributes

    def get_attribute_value(self, attribute_key):
        """
        Given an attribute key, accesses and returns the corresponding attribute value
        """
        return self.attributes[attribute_key]  # return the attribute value

    def get_source_node(self):
        """
        Returns the source node of the edge
        """
        return self.source_node  # return the source node

    def get_terminal_node(self):
        """
        Returns the terminal node of the edge
        """
        return self.terminal_node  # return the terminal node

    def set_weight(self, weight):
        """
        Given a weight value, sets the input as the current weight value of the edge
        """
        self.weight = weight  # overwrite the existing weight with the input weight value

    def set_attributes(self, attributes):
        """
        Given a registry of attributes, sets the input as the registry of current attributes of the edge
        """
        self.attributes = attributes  # overwrite the existing registry of attributes with the input attributes

    def set_attribute_value(self, attribute_key, attribute_value):
        """
        Given an attribute key-value pair, adds the pair to the registry. If an identical attribute key
        exists, the corresponding attribute value is overwritten with the input value
        """
        self.attributes[attribute_key] = attribute_value  # adds the input key-value pair to the registry

    def set_source_node(self, source_node):
        """
        Given a source Node object, sets the input as the current source node of the edge
        """
        self.source_node = source_node  # overwrite the existing source node with the input source Node object

    def set_terminal_node(self, terminal_node):
        """
        Given a terminal Node object, sets the input as the current terminal node of the edge
        """
        self.terminal_node = terminal_node  # overwrite the existing terminal node with the input terminal Node object

