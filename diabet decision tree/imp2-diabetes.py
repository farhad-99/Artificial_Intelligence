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
    
    def append_nextdecision(self, nextdecision):
        self.nextdecision_=(nextdecision)  
          
    def set_currenstate(self, currenstate):
        self.currenstate_ = currenstate  

    def set_name(self, name):
        self.name_ = name  

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
            root.append_nextdecision('Yes')
        else:
            root.append_nextdecision('No')
        return root
        
    p = data[data.out == 1].shape[0]
    n = data[data.out == 0].shape[0]
    root.set_B(round(B(p/(p+n)),3))
    if B(p/(p+n)) == 0:
        if n==0:
            root.append_nextdecision('Yes')
        else:
            root.append_nextdecision('No')
        return root
    max_A = best_attribute(data)
    #root.set_gain(round(gain(data,max_A),3))
    root.append_nextdecision(max_A)
    subdecisions_ = data[max_A].unique()
    for subdecisions in subdecisions_:
        child2 = Node(root,subdecisions,"",[])
        newdata = data[data[max_A]==subdecisions]
        try:
            nd = deepcopy(newdata)
            nd.pop(max_A)
            child2 = create_tree(nd,child2,max_iterate-1)
        except KeyError:    
            child2 = create_tree(nd,child2,max_iterate-1)
        child2.set_gain(round(gain(data,max_A),3))
        root.append_child(child2)


    return root

#display given tree
def display_tree(root,dict,n):
    name = 'a'
    root.set_name(name)
    stack = [root]
    dot = graphviz.Digraph('diabetes decision tree', comment='The Round Table') 
    while stack != []:
        for child in stack[0].child_:
            if stack[0].name_ == 'a':
                name = chr(ord(name)+1)
                child.set_name(name) 
                dot.node(child.name_,  child.nextdecision_+'\n' + 'B(p) ='+str(child.B_)+'\n' + 'G(A) ='+str(child.gain_))  
                dot.node(stack[0].name_ ,stack[0].nextdecision_ +'\n' + 'B(p) ='+str(stack[0].B_)+'\n' + 'G(A) ='+str(stack[0].gain_))
                start = stack[0].name_ 
                end = child.name_
                dot.edge(start, end,translate(dict,stack[0].nextdecision_,child.currentstate_),fontsize = '10',fontcolor='darkblue')
            else:
                name = chr(ord(name)+1)
                child.set_name(name)
                dot.node(child.name_, child.nextdecision_+'\n' + 'B(p) ='+str(child.B_)+'\n' + 'G(A) ='+str(child.gain_))  
                start = stack[0].name_ 
                end = child.name_
                dot.edge(start, end,translate(dict,stack[0].nextdecision_,child.currentstate_),fontsize = '10',fontcolor='darkblue')
                
            stack.append(child)
        stack.pop(0)

    dot.render(directory='diabetes decision tree with n='+str(n), view= False).replace('\\', '/')
    return

#using to decode the digitized values
def translate(dict,dec,current):
    return dict[dec][current]

#digitize the continuous domain with given step
def digit(m,step):
    min1 = np.min(m)
    a = m-min1-0.1
    a = a/step
    return a.astype(int)




data = pd.read_csv('diabetes.csv')
headers = list(data.columns)
size_head = len(headers)-1
headers = headers[0:size_head]
newdata = pd.DataFrame()
dict = pd.DataFrame()
for header in headers:
    m = list(data[header])
    max1 = np.max(m)
    min1 = np.min(m)
    n = 1
    step = (max1 - min1)/n
    s =[]
    for i in range(n):
        s.append(str(round(i*step+min1,2))+'-'+str(round((i+1)*step+min1,2)))
    x = digit(m,step)
    newdata[header] = x
    dict[header] = s



newdata['out'] = list(data['Outcome'])
head = newdata.columns
debaug = deepcopy(newdata[0:1])*0
root = Node(None,'rootc','rootn',[])



root = create_tree(newdata[0:600],root,size_head) 
display_tree(root,dict,n)


test_ = newdata[600:768]
trues =0
notfounded = 0
j=[]
for i in range(168):
    test = test_[i:i+1]
    decision = root.nextdecision_
    nroot = deepcopy(root)
    #print(decision)
    while decision!='Yes' and decision !='No':
        currentstate = list(test[decision])[0]
        #print(currentstate,translate(dict,decision,currentstate))
        ischild =0
        for child in nroot.child_:
            if(child.currentstate_ == currentstate):
                decision = child.nextdecision_
                ischild=1
                #print(decision)
                newroot = child
        if ischild==0:
           
            decision = child.nextdecision_
            #decision = 'Yes'
            ischild=1
            #print(decision)
            newroot = child
            notfounded +=1
        nroot = newroot
    check = list(test['out'])[0]
    if (decision =='Yes' and check ==1) :
        trues +=1
    elif (decision =='No' and check ==0) :
        trues +=1
    else:
        debaug=debaug.append(test,ignore_index=False)
        j.append(i)
print("for n=",n,"test accuracy :",trues*100/168)

x=5