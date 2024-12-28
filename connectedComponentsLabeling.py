# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 15:11:11 2020

@author: Youri.Baeyens
"""
import pandas as pd
import typing

class connectedComponentsLabeler(object):

    """
    A tool to identify the connected components of an undirected graph. 
    """

    nodes = []  
    node2position = {}  
    numberOfNodes = 0
    forest = []

    def __init__(self, edges: pd.DataFrame ):
    
        """
        :parameter edges:  ddges is a Pandas DataFame (two columns named "a" and "b").       
        """
        self.nodes = [node for node in set(edges["a"]).union(edges["b"])]

        self.numberOfNodes = len(self.nodes)

        '''
        A forest is a collection of trees.
        In the end, every connected component will have its own tree.
        A connected component will be identified by the root of its tree (a tree has only one root).
        
        Our forest is implemented with an array.
        There is one array element for every node of our undirected graph.
        The `node2position[A]` dictionary will be used to find the position in the array of node A.
        
        Array elements contain pointers.
        Pointers can be used to jump from one array element to the other, ie, from one node to the other.
        All the nodes that you visit during the journey belong to the same connected component.

        The `findTreeRoot(position)` function can be used to jump from one array element to the other until
        you reach a node that points to itself, ie, until you reach the root of the tree.
        
        We initialize here our array elements: every node points to itself. After this initialisation phase
        will come the phase where we'll build the forest.
        '''
        
        self.forest = [i for i in range(self.numberOfNodes)]

        '''
        As mentionned above, every node has a dedicated array element.
        We create here a dictionary that maps every node to its corresponding array position
        '''
        
        for (position, node) in enumerate(self.nodes):
            self.node2position[node] = position

        '''
        Let us now find the connected components of the undirected graph. This is where we'll build the forest.       
        To do so, we iterate through the edges. If there is an edge between A and B, it means that 
        A and B belong to the same connected component. We'll have to store this knowledge in our forest.
        
        With the `link` function, we use the current
        version of the forest to findTreeRoot(A) and findTreeRoot(B):
         - If the roots are the same, then the current version of the forest already identifies A and B
           as being part of the same connected component. In that case, we don't have to update the forest.
         - If the roots differ, the we'll have to update the forest. At the end of the update
           operation, A and B should have the same tree root.
        
        See docstring of link function.
        '''
        
        for row in edges.itertuples():
            self.link(self.node2position[row.a], self.node2position[row.b])

        '''
        When the loop is over, our forest is up to date : take whatever
        node and travel to its root with the `findTreeRoot` function
        to identify the connected component it belongs to. 
        '''

    def findTreeRoot(self, node):

        """
        The `findTreeRoot(nodePosition)` function can be used to jump from one array element to the other until
        you reach a node that points to itself, ie, until you reach the root of the tree.  

        This implementation of `findTreeRoot` is based on list traversal. There is also a recursive implementation
        of the function.
        """
        
        visitedNodes=[] # Trick to improve performance. See next docString.    
        while self.forest[node] != node:
            visitedNodes.append(node) # Trick to improve performance. See next docString.
            node=self.forest[node]
        treeRoot=node # When forest[node] = node, then we have identified the tree root.
        
        '''
        Let us restructure the tree so that every node directly points to the tree root.
        This steps is only to improve the performance of the algorithm.
        '''
        
        for n in visitedNodes:
            self.forest[n]=node
        
        return treeRoot
            
    def link(self, nodeA, nodeB):
        """
        Link two nodes.

        If node A is linked with B, then they belong to the same
        connected component.

        If findTreeRoot(A) != findTreeRoot(B)
        then we have to correct findTreeRoot().

        This function actually "corrects" the output returned by 
        the findTreeRoot() function.

        """
        ccA = self.findTreeRoot(nodeA)
        ccB = self.findTreeRoot(nodeB)
        if ccA != ccB:
            self.forest[ccA] = ccB

    def getConnectedCompontents(self):

        return pd.DataFrame({'nodeId': self.nodes, 
                             'componentId': [self.findTreeRoot(i) for i in range(self.numberOfNodes)]
                            })
