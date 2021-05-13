"""
File: testAVLtree.py

Tests the AVL tree building algorithm
"""
import random, math

outputdebug = True 

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
            debug("Inserted key [" + str(key) + "]")
            
        #else if there is a value there
        #if less
        elif key < tree.key: 
            self.node.left.insert(key)
        #else if greater
        elif key > tree.key: 
            self.node.right.insert(key)
        # else thing is already in the tree
        else: 
            debug("Key [" + str(key) + "] already in tree.")
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
    
    def logical_successor(self, node):
        ''' 
        Find the smallese valued node in RIGHT child
        ''' 
        node = node.right.node  
        if node != None: # just a sanity check  
            
            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
    
        return inlist 

    #so far we are finding the target
    def delete(self, target):
        print("self.node.key = ", self.node.key)
        if self.node.key == target:
            return self
        elif target < self.node.key:
            if self.node.left is not None:
                self.node.left.delete(target)
        elif target > self.node.key:
            if self.node.right is not None:
                self.node.right.delete(target)
        return None

    
    
    def display(self, level=0, pref=''):
        '''
        Display the whole tree (but turned 90 degrees counter-clockwisely). Uses recursive def.
        '''        
        self.update_heights()  # Must update heights before balances 
        self.update_balances()  
        if(self.node != None): 
            print ('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", 'L' if self.is_leaf() else ' ')    
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')
        



# Usage example
if __name__ == "__main__": 
    a = AVLTree()
    print ("----- Inserting -------")
    #inlist1 = [5, 2, 12, -4, 3, 21, 19, 25]
    #b=AVLTree(inlist1)
    #b.display()
    
    inlist = [55, 81, 65, 20, 35, 79, 23, 14, 21, 103, 92, 45, 85, 51, 47, 48, 50, 46 ]
    print(inlist)
    for i in inlist: 
        a.insert(i)
    print ("Inorder traversal:", a.inorder_traverse())
         
    a.display()
   
    


#def main(size = 20, sort = heapSort):
#   lyst = []
#    for count in range(size):
#        lyst.append(random.randint(1, size*5 + 1))
#    print(lyst)
#    sort(lyst)
#    print(lyst)

#if __name__ == "__main__":
#    main() 
