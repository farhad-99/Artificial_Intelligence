from math import cos,sin,log10,pi
from matplotlib import pyplot as plt
import numpy as np
import random
import pandas as pd
import copy
import time

class Node:
    def __init__(self, data, left=None, right=None,children =0):
        self.data = data
        self.left = left
        self.right = right
        self.children = 0




def generate(): #simple tree generating
    operand = random.random()
    root =[]
    if(operand <1/6):
        root = Node('+')
        root.left =Node('x')
        root.right = Node(str(random.random() * random.randint(-50,100)))
    elif(operand < 2/6):
        root = Node('-')
        if(random.random() < 1/2):
            root.left = Node('x')
            root.right = Node(str(random.random() * random.randint(-50,100)))
        else:
            root.right = Node('x')
            root.left = Node(str(random.random() * random.randint(-50,100)))
    elif(operand < 3/6):
        root = Node('*')
        root.left =Node('x')
        root.right = Node(str(random.random() * random.randint(-50,100)))
    elif(operand < 4/6):
        root = Node('/')
        if(random.random() < 1/2):
            root.left = Node('x')
            root.right = Node(str(random.random() * random.randint(-50,100)))
        else:
            root.right = Node('x')
            root.left = Node(str(random.random() * random.randint(-50,100)))
    elif(operand < 5/6):
        if(random.random()<1/2):
            a = Node('sin')     
        else:
            a = Node('cos')
        b = Node('*')
        b.left = Node('x')
        b.right = Node(str(random.random() * random.randint(-3,3)))
        a.left = b
        root = Node('*')
        root.left = a
        root.right =Node(str(random.random() * random.randint(-3,3)))
        
    else:
                   
        root = Node('^')
        if(random.random() < 1/2):
            root.left = Node('x')
            root.right = Node(str(random.random() * random.randint(-50,50)))
        else:
            root.right = Node('x')
            root.left = Node(str(random.random() * random.randint(-50,50)))
    return root

def isLeaf(node): #checking if the node is leaf or not
    return node.left is None and node.right is None
 
def operation_disp(op, x, y): #displaying a simple operation
    if op == '+':
        return '('+ x + ' + ' + y+')'
    if op == '-':
        return '('+ x + ' - ' + y+')'
    if op == '*':
        return '('+ x + ' * ' + y+')'
    if op == '/':
        return '('+ x + ' / ' + y+')'
    if op == '^':
        return '('+ x + ' ^ ' + y+')'
    if op == 'cos':
        return 'cos(' + x + ')'
    if op == 'sin':
        return 'sin(' + x + ')'
 
def display(root): #display the relation of the tree evaluation function
 
    
    if root is None:
        return 
   
    if isLeaf(root):
        return (root.data)

    xl = display(root.left)
    yl = display(root.right)
    return operation_disp(root.data, xl, yl)

def getElements(root): #finding number of root's elemnets

	if root == None:
		return 0
		
	return (getElements(root.left) +
			getElements(root.right) + 1)

def insertChildrenCount(root): #calculate the number of each node's children

	if root == None:
		return

	root.children = getElements(root) - 1
	insertChildrenCount(root.left)
	insertChildrenCount(root.right)

def children(root): #children +1

	if root == None:
		return 0
	return root.children + 1

def process(op, x, y): # process for each node
    if op == '+':
        return x + y
    if op == '-':
        return x - y
    if op == '*':
        return x * y
    if op == '/':
        if y==0:
            return 100
        return x / y
        
    if op == 'cos':
        return cos(x)
    if op == 'sin':
        return sin(x)
    if op == '^':
        if(x==0):
            return 0
        try:
            return abs(x**abs(y))
        except OverflowError:
            return 100000

def evaluate(root,x): #finding to value of the evaluation tree for input x
 
    
    if root is None:
        return 0
 
    if isLeaf(root):
        if(root.data == 'x'):
            return x
        return float(root.data)
   
    xl = evaluate(root.left,x)
    yl = evaluate(root.right,x)
 
    
    return process(root.data, xl, yl)

vevaluate = np.vectorize(evaluate) #vectroize to evaluate function for faster process

def randomNode(root,move, count): #finding a random node and the path of moving to this node

	if root == None:
		return 0

	if count == children(root.left):
		return move,root

	if count < children(root.left):
		return randomNode(root.left,move+'l', count)

	return randomNode(root.right,move+'r',count - children(root.left) - 1)

def change(deep1,move,rand): #replace a certain node with rand
    if(len(move)==1):
        deep1 = rand
        return deep1
    if(move[0]=='r'):
        deep1.right = change(deep1.right,move[1::],rand)
    else:
       deep1.left =  change(deep1.left,move[1::],rand)
    return deep1

def make_children(root1,root2): #creating 2 children for parents(root1&2)
    move1 =''
    move2 = ''
    count1 = random.randint(0, root1.children)
    count2 = random.randint(0, root2.children)
    move1,rand1 = randomNode(root1,move1,count1)
    move2,rand2 = randomNode(root2,move2,count2)
    move1 = move1+'F'
    move2 = move2+'F'
    parent1 = copy.deepcopy(root1)
    parent2 = copy.deepcopy(root2)
    child1 = change (parent1,move1,rand2)
    child2 = change (parent2,move2,rand1)
    return child1,child2

def new_gen(check1,trees1):# finding the most relative functions for the next generation
    
    df = pd.DataFrame({'val':check1,'trees':trees1})
    dfsort = df.sort_values("val",ascending=True)
    check = dfsort['val'].to_numpy()
    trees = dfsort['trees'].to_list()
    
    parents = trees[0:20]
    prob = check[0:20]
    return prob,parents

def mutation(root,parent,chance):#applying mutation to childrens with a certain chance
    tmp = copy.deepcopy(root)
    if(random.random()<chance):
        move =''
        count = random.randint(0, root.children)
        move , a = randomNode(root,move,count)
        move = move +  'F'
        i = random.randint(0,19)
        change(tmp,move,parent[i])
    return tmp
     

if __name__ == '__main__':
    start = time.time()
    x = np.arange(-2*pi,2*pi,0.1)
    #x = np.arange(0.1,1000,10)
    main = x*np.sin(x)
    #main =x*x +5 
    #main = x*np.cos(x)
    #main = 6/x
    #main = np.sin(5*x + 5)  + np.cos(2*x) 
    #main = np.log10(x)
    main = np.transpose(main)
    for k in range(5):
        maintik = 0
        trees =[]
        y = []
        check = []
        for i in range(200):
            root = generate()
            insertChildrenCount(root)
            print(i,'The  expression tree is', display(root))
            y.append(vevaluate(root,x))
            dist = np.power(y[i]-main,2)
            check.append(np.sum(dist/np.abs(main)))
            trees.append(root)

        prob1,parents = new_gen(check,trees)
        parents1 = copy.deepcopy(parents)
        
        for j in range(10):
            chance = 2*j/100
            children1 = []
            y1=[]
            check1=[]
            tik=0
            for i in range(50):
                p1 =random.randint(0,19)
                p2 = random.randint(0,19)
                child1,child2 = make_children(parents1[p1],parents1[p2])
                insertChildrenCount(child1)
                insertChildrenCount(child2)
                child1 = mutation(child1,parents,chance)
                child2 = mutation(child2,parents,chance)
                
                insertChildrenCount(child1)
                insertChildrenCount(child2)
                children1.append(child1)
                children1.append(child2)
                try:
                    y1.append(vevaluate(child1,x))
                except OverflowError:
                    y1.append(10000)
                try:
                    y1.append(vevaluate(child2,x))
                except OverflowError:
                    y1.append(10000)
                dist1 = np.power(y1[2*i]-main,2)/np.abs(main)
                dist2 = np.power(y1[2*i+1]-main,2)/np.abs(main)
                if(np.sum(dist1)/len(x) < 0.1) :
                    parents1[0] = child1
                    #print('The  expression tree is', display(parents1[0]))
                    tik = 1
                    print(j)
                    j=10
                    i=80
                    break

                elif(np.sum(dist2)/len(x) < 0.1) :
                    parents1[0] = child2
                    #print('The  expression tree is', display(parents1[0]))
                    tik = 1
                    print(j)
                    j=10
                    i=80
                    break

                check1.append(np.sum(dist1))
                check1.append(np.sum(dist2))
            if (tik ==0):
                prob1,parents1 = new_gen(check1,children1)
            else :
                maintik=1
                break
    
        if(maintik ==1):
            break

    print('The  expression tree is', display(parents1[0]))
    print('time of process is:',time.time()-start)
    plt.plot(x,vevaluate(parents1[0],x), x ,main,'r--')
    plt.show()
    te= 5
    