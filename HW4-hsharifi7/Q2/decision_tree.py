from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []

        self.tree = {}
        pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)

        # Let's make sure if we are at the bottom of the tree or not.
        if len(set(y)) == 1:
            self.tree['label'] = y[0]
            return

        # This is when there is an error
        if len(set(y)) == 0:
            self.tree['label'] = 0
            return

        # Keep record of information gain and get the max
        maxIG = -1
        split_attribute = -1

        # This can be categorial or numerical
        split_val = None
        x_left = y_left = x_right = y_right = ([] for i in range(4)) #a new way to initialize array
        
        # find the maximum information gain
        # traverse through nodes, calculate the information gain for each node (parent)
        # pick the maximum IG 
        for i in range(len(X)):
            for j in range(len(X[0])):
                # value to split on
                currentSplitValue = X[i][j]

                # do the split 
                xLeft, xRight, yLeft, yRight = partition_classes(X, y, j, currentSplitValue)
                currentSplitLabels = [yLeft, yRight]

                currentIG = information_gain(y, currentSplitLabels)
                if currentIG > maxIG:
                    maxIG = currentIG
                    split_attribute = j #index of the attribute
                    split_val = currentSplitValue
                    x_left = xLeft
                    y_left = yLeft
                    x_right = xRight
                    y_right = yRight

        # Now that we know the best split, let the split begin!!!
        # Firstly, each left and right are one decistion tre
        self.tree['left'] = DecisionTree()
        self.tree['right'] = DecisionTree()

        # We know what is the attribute and the value we are splitting
        self.tree['attribute'] = split_attribute
        self.tree['value'] = split_val

        # Let's recursively find the best split for each 
        # left and right sides
        self.tree['left'].learn(x_left, y_left)
        self.tree['right'].learn(x_right, y_right)


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted 

        # We pick the top node of our decision tree and call it parent
        # We already know the split attribute and value to split on
        # Make sure to know what type of elemnt is that we are splitting.
        parent = self.tree

        while 'value' in parent:
            split_attribute = parent['attribute']
            split_value = parent['value']

            # Categorial or numerical?
            if isinstance(record[split_attribute], int):
                if record[split_attribute] <= split_value:
                    parent = parent['left'].tree
                else:
                    parent = parent['right'].tree
            else:
                if record[split_attribute] == split_value:
                    parent = parent['left'].tree
                else:
                    parent = parent['right'].tree

        # This is the final label or y
        return parent['label']
