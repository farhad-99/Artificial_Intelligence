import numpy as np
import pandas as pd
import graphviz
from math import log2
from copy import deepcopy

class Node:
    def __init__(self, parent,currenstate,nextdecision,child=None):
        self.parent_ = parent
        self.currentstate_ = currenstate
        self.nextdecision_ = nextdecision
        self.child_ = child
        self.name_ = ""
        self.gain_ = 0
        self.B_ = 0
        

    def append_child(self, child):
        self.child_.append(child)  
    
    def set_nextdecision(self, nextdecision):
        self.nextdecision_=(nextdecision)  

    def set_name(self, name):
        self.name_ = (name)  

    def set_gain(self, gain):
        self.gain_ = gain

    def set_B(self, B):
        self.B_ = B  

# calculate the binary entropy with probability of P
def B(p):
    if p==1 or p==0:
        return  0
    return -(p*log2(p) + (1-p)*log2(1-p))

# calculate the remainder of attribute A in in given data
def remainder(data,A):
    tag = data[A].unique()
    ndata = data.shape[0]
    remainder = 0
    for label in tag:
        tags = data[data[A] == label]
        pk = tags[tags.out == 1].shape[0]
        nk = tags[tags.out == 0].shape[0]
        a = pk/(pk+nk)
        remainder += ((pk+nk)/ndata)*B(a)
    return remainder

# calculate the gain of attribute A in in given data
def gain(data,A):
    p = data[data.out == 1].shape[0]
    n = data[data.out == 0].shape[0]

    gain = B(p/(p+n)) - remainder(data,A)
    return gain

#find the best attribute in given data
def best_attribute(data):
    headers = list(data.columns)

    size_head = len(headers)
    headers = headers[0:size_head-1]
    size_head = len(headers)
    gains = np.zeros((1,size_head),dtype=float)
    i=0
    for A in headers:
        gains[0,i]=(gain(data,A))
        i=i+1

    x = pd.DataFrame(gains,columns=headers)
    max_A = x.idxmax(axis=1)[0]
    return max_A

#create the decision tree for given data with maximum depth of max_iterate
def create_tree(data,root,max_iterate):
    if max_iterate == 0:
        p = data[data.out == 1].shape[0]
        n = data[data.out == 0].shape[0]
        root.set_B(round(B(p/(p+n)),3))
        
        if p>n:
            root.set_nextdecision('Yes')
        else:
            root.set_nextdecision('No')
        return root
        
    p = data[data.out == 1].shape[0]
    n = data[data.out == 0].shape[0]
    root.set_B(round(B(p/(p+n)),3))
    
    if B(p/(p+n)) == 0:
        if n==0:
            root.set_nextdecision('Yes')
        else:
            root.set_nextdecision('No')
        
        return root
        
    max_A = best_attribute(data)
    root.set_gain(round(gain(data,max_A),3))
    root.set_nextdecision(max_A)
    subdecisions_ = data[max_A].unique()
    for subdecisions in subdecisions_:
        child2 = Node(root,subdecisions,"",[])
        newdata = data[data[max_A]==subdecisions]
        try:
            nd = deepcopy(newdata)
            nd.pop(max_A)
            child2 = create_tree(nd,child2,max_iterate-1)
        except KeyError:    
            child2 = create_tree(nd,child2,max_iterate)
        #child2.set_gain(round(gain(data,max_A),3))
        #child2.set_gain(5)
        root.append_child(child2)


    return root

#display given tree
def display_tree(root):
    name = 'a'
    root.set_name(name)
    stack = [root]
    dot = graphviz.Digraph('restaurant decision tree', comment='The Round Table') 
    while stack != []:
        for child in stack[0].child_:
            if stack[0].name_ == 'a':
                name = chr(ord(name)+1)
                child.set_name(name)
                
                dot.node(child.name_,  child.nextdecision_+'\n' + 'B(p) ='+str(child.B_)+'\n' + 'G(A) ='+str(child.gain_))  
                dot.node(stack[0].name_ ,stack[0].nextdecision_ +'\n' + 'B(p) ='+str(stack[0].B_)+'\n' + 'G(A) ='+str(stack[0].gain_))
                start = stack[0].name_ 
                end = child.name_
                dot.edge((start), (end), str(child.currentstate_) )
                
            else:
                name = chr(ord(name)+1)
                child.set_name(name)
                dot.node(child.name_, child.nextdecision_+'\n' + 'B(p) ='+str(child.B_)+'\n' + 'G(A) ='+str(child.gain_))  
                start = stack[0].name_ 
                end = child.name_
                dot.edge((start), (end),str(child.currentstate_) )
            stack.append(child)
        stack.pop(0)

    dot.render(directory='restaurant decision tree', view= True).replace('\\', '/')
    return


data = pd.read_csv('restaurant.csv')
headers = list(data.columns)
size_head = len(headers)-1


root = Node(None,'rootc','rootn',[])
root = create_tree(data,root,size_head) 
display_tree(root)

x=5