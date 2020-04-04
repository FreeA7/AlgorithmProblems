# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:19:39 2020

@author: 98732
"""


class RedBlackTree(object):
    def __init__(self, value, parent=None):
        self.value = value
        self.color = 0
        self.left = None
        self.right = None
        self.parent = parent
        
    def isLeft(self):
        return self == self.parent.left
        
    def getUncle(self):
        if self.parent.isLeft():
            return self.parent.parent.right
        else:
            return self.parent.parent.left
        
    def getSibling(self):
        if self.isLeft():
            return self.parent.right
        else:
            return self.parent.left
        
    @staticmethod
    def rotate(node, direction):
        if direction == 'left':
            if node.parent and node.isLeft():
                node.right.parent, node.parent.left, node.right, node.parent = node.parent, node.right, node.right.left, node.right
            elif node.parent and not node.isLeft():
                node.right.parent, node.parent.right, node.right, node.parent = node.parent, node.right, node.right.left, node.right
            elif not node.parent:
                node.right.parent, node.right, node.parent = node.parent, node.right.left, node.right   
            if node.parent.left:
                node.parent.left.parent = node
            node.parent.left = node
        elif direction == 'right':
            if node.parent and node.isLeft():
                node.left.parent, node.parent.left, node.left, node.parent = node.parent, node.left, node.left.right, node.left
            elif node.parent and not node.isLeft():
                node.left.parent, node.parent.right, node.left, node.parent = node.parent, node.left, node.left.right, node.left
            elif not node.parent:
                node.left.parent, node.left, node.parent = node.parent, node.left.right, node.left   
            if node.parent.right:
                node.parent.right.parent = node
            node.parent.right = node
            
    @staticmethod
    def replaceDeletedNode(node, replacement):
        # We choose successor, so replacement only could has right child
        # 1. Set child of parent of replacement as right child of replacement
        # 2. Set child of parent of node we deleted as replacement
        # 3. Set parent of replacement as parent of node we deleted
        # 4. Set children of replacement as children of node we deleted
        # 5. Set parent of children of node we deleted as replacement
        # 6. Set parent of right child of replacement as parent of replacement
        if replacement:
            replacement.color = node.color
            if replacement.right:
                replacement.right.parent = replacement.parent
            if node.parent and node.isLeft():
                if replacement.isLeft():
                    node.parent.left, replacement.parent, replacement.parent.left, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
                else:
                    node.parent.left, replacement.parent, replacement.parent.right, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
            elif node.parent and not node.isLeft():
                if replacement.isLeft():
                    node.parent.right, replacement.parent, replacement.parent.left, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
                else:
                    node.parent.right, replacement.parent, replacement.parent.right, replacement.left, replacement.right = replacement, node.parent, replacement.right, node.left, node.right
            elif not node.parent:
                if replacement.isLeft():
                    replacement.parent, replacement.parent.left, replacement.left, replacement.right = node.parent, replacement.right, node.left, node.right
                else:
                    replacement.parent, replacement.parent.right, replacement.left, replacement.right = node.parent, replacement.right, node.left, node.right
            if replacement.left:
                replacement.left.parent = replacement
            if replacement.right:
                replacement.right.parent = replacement 
        else:
            # Node must has parent. If node is root, won't call this function
            if node.isLeft():
                node.parent.left = None
            else:
                node.parent.right = None
            
    def inorderNode(self):
        if self.left:
            for node in self.left.inorderNode():
                yield node
        yield self
        if self.right:
            for node in self.right.inorderNode():
                yield node
        
    def inorderPrint(self):
        if self.left:
            self.left.inorderPrint()
        if self.color:
            print('%d Red'%self.value, end=' | ')
        else:
            print('%d Black'%self.value, end=' | ')
        if self.right:
            self.right.inorderPrint()
            
    def standardBSTInsert(self, value):
        # Empty tree
        if self.value == None:
            return RedBlackTree(value, None)
        if value < self.value:
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
        inorder = self.inorderNode()
        while 1:
            try:
                node = inorder.__next__()
            except StopIteration:
                node = None
                break
            if node.value == value:
                break
        # The value dosen't exist in the tree
        if not node:
            raise KeyError('The value dosen\'t exist in the tree!')
        # Node is root and root is a leaf
        if node.parent == None:
            return None, None, None
        # Node is a leaf node
        if not node.left and not node.right:
            return node, None, None
        # Node has only right child
        elif not node.left and node.right:
            return node, node.right, None
        # Node has only left child
        elif node.left and not node.right:
            return node, node.left, None
        # Node has two children and it must have successor
        elif node.left and node.right:
            # Successor is chosen as replacement
            replacement = inorder.__next__()
            # Replacement is a leaf node
            if not replacement.left and not replacement.right:
                return node, replacement, None
            # For replacement is a successor of node we deleted
            # It only could be a leaf node or a node with only right child
            # If it has left child, then the left child must be the real successor of node we deleted
            # Vice versa, if we choose the predecessor as replacement
            # The predecessor either is a leaf or only has left child
            else:
                return node, replacement, replacement.right
     
    def insert(self, value):
        # Standard BST insertion doesn't motify entire root
        node = self.standardBSTInsert(value)
        node.color = 1
        
        # Check is there two consecutive reds in RedBlackTree
        # Empty Tree Insertion [No two consecutive reds] ==> Done
        # Node is root [No two consecutive reds] => Done
        while node.parent:
            # The parent's color is black [No two consecutive reds] => Done
            if node.parent.color == 0:
                return
            uncle = node.getUncle()
            # The color of uncle is black (Null is black)
            if not uncle or uncle.color == 0:
                # left left
                if node.parent.isLeft() and node.isLeft():
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    RedBlackTree.rotate(node.parent.parent, 'right')
                    return
                # left right
                elif node.parent.isLeft() and not node.isLeft():
                    RedBlackTree.rotate(node.parent, 'left')
                    node.color = 0
                    node.parent.color = 1
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
                    node.color = 0
                    node.parent.color = 1
                    RedBlackTree.rotate(node.parent, 'left')
                    return
            # The color of uncle is red
            else:
                uncle.color = 0
                node.parent.color = 0
                node.parent.parent.color = 1
                node = node.parent.parent
        # Motify the color of root as black
        node.color = 0
        return
    
    def delete(self, value):
        node, replacement, x = self.standardBSTDeletion(value)
        # Delete root and root is a leaf
        if not node:
            self.value = None
            return
        # Node we deleted is red, replacement is red or Null
        if node.color == 1:
            if not replacement or replacement.color == 1:
                RedBlackTree.replaceDeletedNode(node, replacement)
                return
        # Node we deleted is black, replacement is red
        if node.color == 0 and replacement and replacement.color == 1:
            replacement.color = 0
            RedBlackTree.replaceDeletedNode(node, replacement)
            return
        # Node we delete is red, replacement is black
        # Node we delete is black, replacement is black
        # If replacement is Null, the mininun imbalanced tree after replacing is the subtree whose root is the parent of node we deleted.
        if not replacement:
            sibling = node.getSibling()
            parent = node.parent
        # If replacement is not Null, the mininun imbalanced tree after replacing is the subtree whose root is replacement.
        else:
            sibling = replacement.getSibling()
            parent = replacement.parent
        # Replace node we deleted with replacement      
        RedBlackTree.replaceDeletedNode(node, replacement)
        
        while 1:
            # Case 1: x is red
            if x and x.color == 1:
                x.color = 0
                return
            
            # Case 2: x is black, sibling is red
            if not x or x.color == 0:
                if sibling.color == 1:
                    sibling.color = 0
                    parent.color = 1
                    if sibling.isLeft():
                        RedBlackTree.rotate(parent, 'right')
                        sibling = parent.left
                    else:
                        RedBlackTree.rotate(parent, 'left')
                        sibling = parent.right
                    # ==> case 3,4,5
                    
            # Case 3: x is black, sibling is black and both of its children is black
            if not x or x.color == 0:
                if sibling.color == 0 and (not sibling.left or sibling.left.color == 0) and (not sibling.right or sibling.right.color == 0):
                    sibling.color = 1
                    x = parent
                    sibling = x.getSibling()
                    parent = x.parent
                    if x.color == 1:
                        x.color = 0
                        return 
                    # Get new minimum balanced tree
                    else:
                        # New x is root
                        if not x.parent:
                            return
                        pass
                        # ==> case 2,3,4,5
                
            # Case 4: x is black, sibling is black and the child of sibling which is in the same direction with x is red and the other one is black
            # Get rotation struct [Keeping the black height of sibling remaining]
            if not x or x.color == 0:
                if sibling.color == 0:
                    if sibling.isLeft() and (sibling.right and sibling.right.color == 1) and (not sibling.left or sibling.left.color == 0):
                        sibling.color = 1
                        sibling.right.color = 0
                        RedBlackTree.rotate(sibling, 'left')
                        sibling = sibling.parent
                        # ==> case 5
                    elif not sibling.isLeft() and (sibling.left and sibling.left.color == 1) and (not sibling.right or sibling.right.color == 0):
                        sibling.color = 1
                        sibling.left.color = 0
                        RedBlackTree.rotate(sibling, 'right')
                        sibling = sibling.parent
                        # ==> case 5
                
            # Case 5: x is black, sibling is black and the child of sibling which is not in the same direction with x is red
            if not x or x.color == 0:
                if sibling.color == 0:
                    if sibling.isLeft() and sibling.left and sibling.left.color == 1:
                        sibling.left.color = 0
                        sibling.color = parent.color
                        parent.color = 0
                        RedBlackTree.rotate(parent, 'right')
                        return
                    elif not sibling.isLeft() and sibling.right and sibling.right.color == 1:
                        sibling.right.color = 0
                        sibling.color = parent.color
                        parent.color = 0
                        RedBlackTree.rotate(parent, 'left')
                        return
            
            

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
            if node.value == value:
                break
        node = self.inorder()


redblacktree = RedBlackTree(7)
redblacktree.insert(3)
redblacktree.insert(18)
redblacktree.insert(10)
redblacktree.insert(22)
redblacktree.insert(8)
redblacktree.insert(11)
redblacktree.insert(26)
redblacktree.inorderPrint()
print('\n-------------')
redblacktree.delete(3)
redblacktree.inorderPrint()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            