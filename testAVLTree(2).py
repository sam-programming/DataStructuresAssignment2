"""
File: testAVLtree.py

Tests the AVL tree building algorithm
"""
import random, math

outputdebug = False 

def debug(msg):
    if outputdebug:
        print (msg)
        
#Binary Tree Node with left child and right child
class Node():
    def __init__(self, key):
        self.key = key  #this is the value of the node
        self.left = None 
        self.right = None 


#AVL Tree Class
class AVLTree():
    #self, plus variable number of arguments
    def __init__(self, *args):
        self.node = None  #no nodes
        self.height = -1  #empty tree has a height (depth) of -1
        self.balance = 0; #balance is left_height - right_height

        #if only one argument
        if len(args) == 1: 
            for i in args[0]: 
                self.insert(i) #call insert on that argument
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) #if height is 0, this is a leaf node

    #key is the value to be inserted
    def insert(self, key):
        
        #get the current node
        tree = self.node
        
        #create a new node
        newnode = Node(key)

        #if self.node == None
        if tree == None:
            self.node = newnode   #create new node
            self.node.left = AVLTree()  #instantiate left and right nodes
            self.node.right = AVLTree()
            print("Inserted key [" + str(key) + "]")
            
        #else if there is a value there
        #if less
        elif key < tree.key: 
            self.node.left.insert(key)
        #else if greater
        elif key > tree.key: 
            self.node.right.insert(key)
        # else thing is already in the tree
        else: 
            print("Key [" + str(key) + "] already in tree.")
        #finally call rebalance
        self.rebalance() 
        
    def rebalance(self):
        ''' 
        Rebalance a particular (sub)tree
        '''
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: #if height difference is larger than 1 or -1
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()


    #If left subtree is unbalanced       
    def rrotate(self):
        # Rotate left pivoting on self, an unbalanced part of the tree
        debug ('Rotating ' + str(self.node.key) + ' right')
        #silly debug says it is rotating 1 value but its rotating three
        A = self.node  #a is the node of the tree passed a parameter
        B = self.node.left.node  #b is a's left node
        T = B.right.node         #t is b's right node

        #       A
        #      / 
        #     B   
        #      \
        #       T
        
        self.node = B     #A becomes B
        B.right.node = A  #T becomes A
        A.left.node = T   #B becomes T

        #       B
        #      / \
        #     T   A

    
    def lrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 
        
            
    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 


    def logical_predecessor(self, node):
        ''' 
        Find the biggest valued node in LEFT child
        ''' 
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 

    #Original method not used
    '''
    def logical_successor(self):
         
        Find the smallest valued node in RIGHT child
        
        node = self.node.right.node
        if node != None: # just a sanity check  
            
            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None:
                    print(type(node))
                    return node
                else: 
                    node = node.left.node
        print(type(node))
        return node
    '''
    
    #find and delete the smallest valued node in right child, return the key
    def find_successor(self):
        parent = self.node
        current = self.node.right.node
        iteration = 1
        if current != None:
            while current.left != None:
                if current.left.node == None: #we have found the successor
                    #we need to sever the tie from the parent at parent.left                    
                    key = current.key
                    #if this is the first iteration, it will be parent.right that needs
                    #to be deleted, otherwise parent left will have to be deleted
                    if iteration == 1:
                        parent.right.node = None
                    else:
                        parent.left.node = None
                    return key
                else:
                    #update values
                    iteration += 1
                    parent = current
                    current = current.left.node
        #this return never hits in our code, just in case the method is called elsewhere
        return current.key
                
    
    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            debug("self.node == None")
            return []            
        
        inlist = []
        #UNDESCRIPTIVE VARIABLE NAMES
        l = self.node.left.inorder_traverse()
        debug("L" + str(l))
        for i in l:
            debug("i" + str( i))
            inlist.append(i) 

        inlist.append(self.node.key)
        debug("Self.node.key = " + str(self.node.key))

        r = self.node.right.inorder_traverse()
        debug("R" + str(r))
        for x in r:
            debug("x" + str(x))
            inlist.append(x) 
    
        return inlist 

    def find_leafs(self):
        if self.node == None:
            return []
        leafs = []
        left = self.node.left.find_leafs()
        for val in left:
            leafs.append(val)
            
        if self.is_leaf():
            leafs.append(self.node.key)
        debug(str(self.node.key))

        right = self.node.right.find_leafs()
        for val in right:
            leafs.append(val)
        
        return leafs
        
    def find_parents(self):
        if self.node == None:
            return []
        parents = []
        left = self.node.left.find_parents()
        for val in left:
            parents.append(val)
        
        if not self.is_leaf():
            parents.append(self.node.key)
            debug(str(self.node.key))

        right = self.node.right.find_parents()
        for val in right:
            parents.append(val)

        return parents
    
    #Delete a given element in an AVL Tree
    def delete(self, target):
        # if the value is not in the tree, print message
        if self.node is None:
            print("Value not found")
        #if target is lower, then traverse the left subtree
        elif target < self.node.key:
            self.node.left.delete(target)
        #if target is higher, then traverse the right subtree
        elif target > self.node.key:
            self.node.right.delete(target)
        #found
        else:
            print("Deleting key [" + str(self.node.key) + "]")
            if self.is_leaf():
                debug("Deleting leaf")
                self.node = None
            #node has a right child but not a left child
            elif self.node.right.node is not None and self.node.left.node is None:
                #three way swap
                debug("Swapping right node")
                temp = self.node.right.node
                self.node.right.node = None
                self.node = temp
            elif self.node.right.node is None and self.node.left.node is not None:
                debug("Swapping left node")
                temp = self.node.left.node
                self.node.left.node = None               
                self.node = temp
            #else if the node has two children
            else:
                #get the leftmost leaf of the right tree
                # need to clear the node in the logical_successor method
                # and return the key only
                debug("Swapping logical successor")
                successor = self.find_successor()
                self.node.key = successor
        self.rebalance()
        
    
    def display(self, level=0, pref=''):
        '''
        Display the whole tree (but turned 90 degrees counter-clockwisely). Uses recursive def.
        '''        
        self.update_heights()  # Must update heights before balances 
        self.update_balances()  
        if(self.node != None):
            #This doesn't work on python versions < 3
            print ('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", 'L' if self.is_leaf() else ' ')    
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')
        


# Usage example
if __name__ == "__main__": 
    tree = AVLTree()
    nodes = [50, 30, 70, 20, 40, 60, 80, 37, 36]
    
    
    for i in nodes: 
        tree.insert(i)

    tree.display()
    leafs = tree.find_leafs()
    parents = tree.find_parents()
    print("Leafs:" , leafs)
    print("Parents", parents)
##    tree.display()
##    print("\n")
##    tree.delete(80)
##    print("\n")
##    tree.display()
##    print("\n")
##    tree.delete(70)
##    print("\n")
##    tree.display()
##    print("\n")
##    tree.insert(32)
##    print("\n")
##    tree.insert(32)
##    print("\n")
##    tree.display()
##    print("\n")
##    print("Delete Root")
##    tree.delete(37) #delete root note
##    print("\n")
##    tree.display()
   


