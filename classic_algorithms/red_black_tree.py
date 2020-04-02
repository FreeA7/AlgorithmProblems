# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:19:39 2020

@author: 98732
"""


class Node(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color


class RedBlackTree(object):
    def __init__(self, value, parent):
        self.root = Node(value, 0)
        self.left = None
        self.right = None
        self.parent = parent
        
    def isLeft(self):
        return self == self.parent.left
        
    def getUncle(self):
        if self.parent == self.parent.parent.left:
            return self.parent.parent.right
        else:
            return self.parent.parent.left
        
    def getSibling(self):
        if self == self.parent.left:
            return self.parent.right
        else:
            return self.parent.left
        
    @staticmethod
    def rotate(node, direction):
        if direction == 'left':
            node.right.parent, node.right, node.parent = node.parent, node.right.left, node.right
        elif direction == 'right':
            node.left.parent, node.left, node.parent = node.parent, node.left.right, node.left
            
    def inorder(self):
        if self.left:
            for node in self.left.inorder():
                yield node
        yield self
        if self.right:
            for node in self.right.inorder():
                yield node
            
    def standardBSTInsert(self, value):
        if value < self.root.value:
            if self.left:
                return self.left.standardBSTInsert(value)
            else:
                self.left = RedBlackTree(value, self)
                return self.left
        else:
            if self.right:
                return self.right.standardBSTInsert(value)
            else:
                self.right = RedBlackTree(value, self)
                return self.right
    
    def standardBSTDeletion(self, value):
        inorder = self.inorder()
        while 1:
            node = inorder.__next__()
            if node.root.value == value:
                break
        # Node is a leaf node
        if not node.left and not node.right:
            return node, None, None
        # Node has only right child
        elif not node.left and node.right:
            return node, node.right, None
        # Node has only left child
        elif node.left and not node.right:
            return node, node.left, None
        # Node has two children
        elif node.left and node.right:
            # Successor is chosen as replacement
            replacement = inorder.__next__()
            # Replacement is a leaf node
            if not replacement.left and not replacement.right:
                return node, replacement, None
            # For replacement is a successor of node we deleted
            # It only could be a leaf node or a node with only right child
            else:
                return node, replacement, replacement.right
            
    def insert(self, value):
        # Standard BST insertion doesn't motify entire root
        node = self.standardBSTInsert(value)
        node.root.color = 1
        
        # The parent is entire root => Done
        while node.parent:
            # The parent's color is black => Done
            if node.parent.root.color == 0:
                return
            uncle = node.getUncle()
            # The color of uncle is black (Null is black)
            if not uncle or uncle.root.color == 0:
                # left left
                if node.parent.isLeft() and node.isLeft():
                    node.parent.root.color = 0
                    node.parent.parent.root.color = 1
                    RedBlackTree.rotate(node.parent.parent, 'right')
                    return
                # left right
                elif node.parent.isLeft() and not node.isLeft():
                    RedBlackTree.rotate(node.parent, 'left')
                    node.root.color = 0
                    node.parent.root.color = 1
                    RedBlackTree.rotate(node.parent, 'right')
                    return
                # right right
                elif not node.parent.isLeft() and not node.isLeft():
                    node.parent.root = 0
                    node.parent.parent.root = 1
                    RedBlackTree.rotate(node.parent.parent, 'left')
                    return
                # right left
                elif not node.parent.isLeft() and node.isLeft():
                    RedBlackTree.rotate(node.parent, 'right')
                    node.root.color = 0
                    node.parent.root.color = 1
                    RedBlackTree.rotate(node.parent, 'left')
                    return
            # The color of uncle is red
            else:
                uncle.root.color = 0
                node.parent.root.color = 0
                node.parent.parent.root.color = 1
                node = node.parent.parent
        # Motify the color of entire root as black
        node.root.color = 0
        return
    
    def replaceNode(self, node, replacement):
        if replacement:
            if node.isLeft():
                if replacement.isLeft():
                    node.parent.left, replacement.parent, replacement.parent.left, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
                else:
                    node.parent.left, replacement.parent, replacement.parent.right, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
            else:
                if replacement.isLeft():
                    node.parent.right, replacement.parent, replacement.parent.left, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
                else:
                    node.parent.right, replacement.parent, replacement.parent.right, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
        else:
            if node.isLeft():
                node.parent.left = None
            else:
                node.parent.right = None
    
    def delete(self, value):
        node, replacement, x = self.standardBSTDeletion(value)
        # Node we deleted is red, replacement is red or Null
        if node.root.color == 1:
            if not replacement or replacement.root.color == 1:
                self.replaceNode(node, replacement)
                return
        # Node we deleted is black, replacement is red
        if node.root.color == 0 and replacement.root.color == 1:
            replacement.root.color = 0
            self.replaceNode(node, replacement)
            return
        # Node we delete is red, replacement is black
        # Node we delete is black, replacement is black
        # The sibling and parent of x after replacing are just sibling and parent of replacement
        sibling = replacement.getSibling()
        parent = replacement.parent
        # Replace node we deleted with replacement
        replacement.root.color = node.root.color
        self.replaceNode(node, replacement)
        # Case 1: x is red
        if x and x.root.color == 1:
            x.root.color = 0
            return
        
        # Case 2: x is black, silbing is red
        elif not x or x.root.color == 0:
            if sibling and sibling.root.color == 1:
                sibling.root.color = 0
                parent.root.color = 1
                if sibling.isLeft():
                    RedBlackTree.rotate(parent, 'right')
                    x = parent.left
                else:
                    RedBlackTree.rotate(parent, 'left')
                    x = parent.right
                sibling = x.getSibling()
                parent = x.parent
                
            # Case 3:
            if sibling.root.color == 0:
                if not sibling.left or sibling.left.root.color == 0:
                    if not sibling.right or sibling.right.root.color == 0:
                        
        
                
                
                
        
        
            
            

class BinarySearchTree(object):
    def __init__(self, value, parent):
        self.root = value
        self.left = None
        self.right = None
        self.parent = parent
        
    def inorder(self):
        if self.left:
            for node in self.left.inorder():
                yield node
        yield self
        if self.right:
            for node in self.right.inorder():
                yield node
                
    def insert(self, value):
        if value < self.root:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BinarySearchTree(value, self)
        else:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BinarySearchTree(value, self)
    
    def deletion(self, value):
        for node in self.inorder():
            if node.root.value == value:
                break
        node = self.inorder()

node = BinarySearchTree(1, None)
node.insert(7)
node.insert(3)
node.insert(4)
node.insert(5)
node.insert(6)
node.insert(2)
i = node.inorder()
while 1:
    if i.__next__().root == 2:
        break
#node.left.parent, node.left, node.parent = node.parent, node.left.right, node.left
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            