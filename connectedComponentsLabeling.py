# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 15:11:11 2020

@author: Youri.Baeyens
"""
import pandas as pd

class connectedComponentsLabeler(object):

    """
    A tool to identify the connected components of an undirected graph. 
    """

    edges = pd.DataFrame({})
    nodes = []
    
    node2position = {}
    
    numberOfNodes = 0
    forest = []

    def __init__(self, edges):
    
        """
        :parameter edges:  ddges is a Pandas DataFame (two columns named "a" and "b"). 
        
        """
        self.edges = edges
        
        self.nodes = [node for node in set(self.edges["a"]).union(self.edges["b"])]

        self.numberOfNodes = len(self.nodes)

        '''
        A forest is a collection of trees 
        Every connected component has got its own tree
        Our forest is implemented with an array
        There is one array element for every node of our undirected graph
        Array elements contain pointers
        Pointers can be used to travel from one array element to the other, ie, from one node to the other
        All the nodes that you visit during your journey belong to the same connected component.
        We initialize here our array elements: every node points to itself
        '''
        
        self.forest = [i for i in range(self.numberOfNodes)]

        '''
        Every node has a dedicated array element
        We create here a dictionary that maps every node to its corresponding array position
        '''
        
        for (position, node) in enumerate(self.nodes):
            self.node2position[node] = position

        '''
        Let us identify the connected components
        We iterate through the edges. Each step may require an update of the forest.
        See docstring of link function.
        '''
        
        for row in self.edges.itertuples():
            self.link(self.node2position[row.a], self.node2position[row.b])

        '''
        When the loop is over, our forest is up to date : take whatever
        node and travel to its root with the "connectedComponentIdentifier" function
        to identify the connected component it belongs to. 
        '''

    def connectedComponentIdentifier(self, node):

        """
        Identifies the connected component of a specific node (list implementation).
        """
        
        visitedNodes=[]

        '''
        Jump from one node to the other until you reach a node that points to itself. This
        node identifies the connected component the node belongs to.
        '''
        
        while self.forest[node] != node:
            visitedNodes.append(node)
            node=self.forest[node]

        '''
        Let us restructure the tree so that every node directly points to the tree root (performance improvement)
        '''
        
        for n in visitedNodes:
            self.forest[n]=node
        
        return node
            
    def link(self, nodeA, nodeB):
        """
        Link two nodes.

        If node A is linked with B, then they belong to the same
        connected component.

        If connectedComponentIdentifier(A) != connectedComponentIdentifier(B)
        then we have to correct connectedComponentIdentifier().

        This function actually "corrects" the output returned by 
        the connectedComponentIdentifier() function.

        """
        ccA = self.connectedComponentIdentifier(nodeA)
        ccB = self.connectedComponentIdentifier(nodeB)
        if ccA != ccB:
            self.forest[ccA] = ccB

    def simplifyForest(self):
        """
        Transform the forest into a list.

        Function simplifyForest is used to store the
        connectedComponentIdentifier of every node in forest.

        """
        for i in range(len(self.forest)):
            self.forest[i] = self.connectedComponentIdentifier(i)

    def getConnectedCompontents(self):

        self.simplifyForest()

        return pd.DataFrame({'nodeId': self.nodes, 'componentId': self.forest})
