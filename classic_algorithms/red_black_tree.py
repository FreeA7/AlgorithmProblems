# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:19:39 2020

@author: FreeA7

Red Black Tree
"""

class RedBlackTree(object):
    def __init__(self):
        self.value = None
        self.color = 0
        self.left = None
        self.right = None
        self.parent = None
        
    def __str__(self):
        # Print information(value and color) of self and its parent and its children
        output = 'NodeValue\tNodeColor\n'
        output += '%s\t%s\n'%(str(self.value), str(self.color))
        output += 'ParentValue\tParentColor\n'
        if self.parent:
            output += '%s\t%s\n'%(str(self.parent.value), str(self.parent.color))
        else:
            output += '%s\t%s\n'%(str(None), str(None))
        output += 'LeftValue\tLeftColor\n'
        if self.left:
            output += '%s\t%s\n'%(str(self.left.value), str(self.left.color))
        else:
            output += '%s\t%s\n'%(str(None), str(None))
        output += 'RightValue\tRightColor\n'
        if self.right:
            output += '%s\t%s\n'%(str(self.right.value), str(self.right.color))
        else:
            output += '%s\t%s'%(str(None), str(None))
        return output
        
        
    def isLeft(self):
        # Return the node is the left child of its parent or not
        return self == self.parent.left
        
    def getUncle(self):
        # Get the uncle of node
        if self.parent.isLeft():
            return self.parent.parent.right
        else:
            return self.parent.parent.left
        
    def getSibling(self):
        # Get the sibling of node
        if self.isLeft():
            return self.parent.right
        else:
            return self.parent.left
        
    @staticmethod
    def rotate(node, direction):
        # Rotation
        if direction == 'left':
            # 1. Set parent of right child of node as parent of node
            node.right.parent = node.parent
            # 2. Set child of parent of node as right child of node
            if node.parent and node.isLeft():
                node.parent.left = node.right
            elif node.parent and not node.isLeft():
                node.parent.right = node.right
            # 3. Set parent of node as right child of node
            node.parent = node.right
            # 4. Set right child of node as left child of new parent(right child of node before rotation) of node
            node.right = node.parent.left
            # 5. Set parent of new right child as node
            if node.right:
                node.right.parent = node
            # 6. Set left child of new parent as node
            node.parent.left = node
        elif direction == 'right':
            # 1. Set parent of left child of node as parent of node
            node.left.parent = node.parent
            # 2. Set child of parent of node as left child of node
            if node.parent and node.isLeft():
                node.parent.left = node.left
            elif node.parent and not node.isLeft():
                node.parent.right = node.left
            # 3. Set parent of node as left child of node
            node.parent = node.left
            # 4. Set left child of node as right child of new parent(left child of node before rotation) of node
            node.left = node.parent.right
            # 5. Set parent of new left child as node
            if node.left:
                node.left.parent = node
            # 6. Set right child of new parent as node
            node.parent.right = node
            
    @staticmethod
    def replaceDeletedNode(node, replacement):
        # Replace the node we deleted and replacement
        #   We choose successor in this implement, so replacement only could has right child
        if replacement:
            # 1. Recolor replacement
            replacement.color = node.color
            # 2. Set parent of child of replacement as parent of replacement
            if replacement.right:
                replacement.right.parent = replacement.parent
            # 3. Set child of parent of replacement as child of replacement
            if replacement.isLeft():
                replacement.parent.left = replacement.right
            else:
                replacement.parent.right = replacement.right
            # 4. Set child of parent of node we deleted as replacement
            if node.parent and node.isLeft():
                node.parent.left = replacement
            elif node.parent and not node.isLeft():
                node.parent.right = replacement
            # 5. Set parent of replacement as parent of node we deleted
            replacement.parent = node.parent
            # 6. Set children of replacement as children of node we deleted 
            replacement.left, replacement.right = node.left, node.right
            # 7. Set parent of child of replacement after replacing
            if replacement.left:
                replacement.left.parent = replacement
            if replacement.right:
                replacement.right.parent = replacement
        else:
            # No replacement, node we deleted is leaf not can't be root:
            #   Node must has parent. If node is root, it either has replacement, or it won't call this function(leaf and root)
            if node.isLeft():
                node.parent.left = None
            else:
                node.parent.right = None
        # 8. Set node.color as None means root has been replaced
        node.color = None
            
    def inorderNode(self):
        # Return each node of the tree whose value from small to large
        if self.left:
            for node in self.left.inorderNode():
                yield node
        yield self
        if self.right:
            for node in self.right.inorderNode():
                yield node
            
    def standardBSTInsert(self, value, parent=None):
        # Standard Binary Search Tree Insertion(Return new node of new value):
        #   If self.value == Null, it's a empty tree and we must set value and parent
        #   But if insert() call this function, it won't pass parent.
        #   At this case, if self.value == Null means it's a empty tree
        #   If in the function itself, it will create a new leaf and set it's value and parent
        if self.value == None:
            self.value = value
            self.parent = parent
            return self
        if value < self.value:
            if self.left:
                return self.left.standardBSTInsert(value)
            else:
                self.left = RedBlackTree()
                self.left.standardBSTInsert(value, self)
                return self.left
        elif value > self.value:
            if self.right:
                return self.right.standardBSTInsert(value)
            else:
                self.right = RedBlackTree()
                self.right.standardBSTInsert(value, self)
                return self.right
        # The value has in the tree
        else:
            raise ValueError('The value has been in the tree!')
    
    def standardBSTDeletion(self, value):
        # Standard Binary Search Tree Deletion
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
        if node.parent == None and not node.left and not node.right:
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
        # Insert a new value into a redblacktree
        
        # Standard BST insertion doesn't motify root
        node = self.standardBSTInsert(value)
        # Set color of new node is red.
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
                    node.parent.color = 0
                    node.parent.parent.color = 1
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
        # Delete a new value into a redblacktree
        
        # Get node we deleted and replacement and x
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
        
        # Node we deleted has been replaced by its child, and its color is None for deleting
        # So the replacement is its child and new parent is replacement
        if parent.color == None:
            parent = replacement
        
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
            # To get rotation struct [Keeping the black height of sibling remaining]
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


class RedBlackTreeCreater(object):
    # Create a red black tree
    def __init__(self):
        self.redblacktree = RedBlackTree()
        self.blackheight = 0
        
    def __returnRoot(self):
        # Action Rotation in Insertion and Deletion may change root of red black tree
        # So we must return the root after insertion and deletion
        while self.redblacktree.parent:
            self.redblacktree = self.redblacktree.parent
        child = self.redblacktree
        if child.value:
            self.blackheight = 1
        else:
            self.blackheight = 0
        while child.left:
            child = child.left
            if not child.color:
                self.blackheight += 1
                
    def __str__(self):
        # Plot red black tree and print the root and the black height of red black tree
        from red_black_tree_plot import RedBlackTreePloter
        output = 'Root: %s \tBlackHeight: %s'%(str(self.redblacktree.value), str(self.blackheight))
        RedBlackTreePloter.showTree(self.redblacktree)
        return output
        
    def insert(self, arg):
        # Insert a value or a array into red black tree
        from numpy import ndarray
        from inspect import isgenerator
        if type(arg) in (list, set, tuple, ndarray) or isgenerator(arg):
            for value in arg:
                self.redblacktree.insert(value)
                self.__returnRoot()
        elif type(arg) == int or type(arg) == float:
            self.redblacktree.insert(arg)
            self.__returnRoot()
        else:
            raise TypeError('The type can\'t be stored in the RedBlackTree!')
            
    def delete(self, value):
        # Delete a value from red black tree
        self.redblacktree.delete(value)
        # root has been replaced
        if self.redblacktree.color == None:
            if self.redblacktree.left:
                self.redblacktree = self.redblacktree.left
            elif self.redblacktree.right:
                self.redblacktree = self.redblacktree.right
        self.__returnRoot()
        
    def savePlot(self, path, name=None):
        # Save plot of the red black tree
        from red_black_tree_plot import RedBlackTreePloter
        if name == None: name = 'root%sblackheight%s'%(str(self.redblacktree.value), str(self.blackheight))
        RedBlackTreePloter.saveTree(self.redblacktree, path, name)
        print('Save successfully: '+path+'Root%sBlackHeight%s'%(str(self.redblacktree.value), str(self.blackheight))+'.png')
        
        
if __name__ == '__main__':    
    PATH = './RedBlackTreeImages/'
    
    # Example 1
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert([7, 3, 18, 10, 22, 8, 11, 26])
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example1Created')
    redblacktree.delete(3)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example1Deleted')
    
    # Example 2
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert([13, 17, 8, 11, 1, 15, 6, 25, 22, 27])
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example2Created')
    redblacktree.delete(11)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example2Deleted')
    
    # Example 3
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert(1)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example3Created')
    redblacktree.delete(1)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example3Deleted')
    
    # Example 4
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example4Created')
    redblacktree.delete(8)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example4Deleted')
                
    # Example 5
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert([13,8,17,1,11,15,25,6,22,27])
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example5Created')
    redblacktree.delete(8)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example5Deleted')
    
    # Example 6
    redblacktree = RedBlackTreeCreater()
    redblacktree.insert(list(range(100,0,-1)))
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example6Created')
    redblacktree.delete(50)
    print(redblacktree)
    redblacktree.savePlot(PATH, 'Example6Deleted')