
import xml.etree.ElementTree as ET
from tkinter import *
import time
import copy
import numpy as np
import random
#------class
class Table:
      
    def __init__(self,root):
          
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if Scan[i][j] == 'blind':
                    self.object = Entry(root, width=5,background='black', fg='black',font=('Arial',16,'bold'))               
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, Scan[i][j])
                elif Scan[i][j] == 'empty':
                    self.object = Entry(root, width=5, fg='white',font=('Arial',16,'bold'))               
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, Scan[i][j])
                elif Scan[i][j] == 'obstacle':
                    self.object = Entry(root, width=5,background='red', fg='red',font=('Arial',16,'bold'))             
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, Scan[i][j])
                elif Scan[i][j] == 'robot' and Map[i][j]=='Battery':
                    self.object = Entry(root, width=5,background='green', fg='black',font=('Arial',16,'bold'))             
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, 'found!')
                elif Scan[i][j] == 'robot' :
                    self.object = Entry(root, width=5,background='blue', fg='black',font=('Arial',16,'bold'))             
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, Scan[i][j])
                elif Scan[i][j] == 'Battery':
                    self.object = Entry(root, width=5,background='green', fg='black',font=('Arial',16,'bold'))             
                    self.object.grid(row=i, column=j)
                    self.object.insert(END, Scan[i][j])
                
                

#------functions

def mov(i1,j1,i2,j2,Map,Scan):
    if Map[i2][j2] =='obstacle':
        Scan[i2][j2] = Map[i2][j2]
    else:
        Scan[i1][j1]='empty'
        Scan[i2][j2]='robot'
    
    return Scan

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)

def find_dist(ist,jst,rows,columns):
    H=np.zeros((rows,columns))
    for i in range(rows):
        for j in range(columns):
            H[i,j] = ((ist-i)**2 + (jst-j)**2) **0.5
    
    return H
def find_next(ist,jst,H,Scan,Map):
    rows,columns = H.shape
    i1 = max(ist-1,0)
    j1 = jst
    h1 = H[i1,j1]
    i2 = ist
    j2 = max(jst-1,0)
    h2 = H[i2,j2]
    i3 = min(ist+1,rows-1)
    j3 = jst
    h3 = H[i3,j3]
    i4 = ist
    j4 = min(jst+1,columns-1)
    h4 = H[i4,j4]
    i = [i1,i2,i3,i4]
    j = [j1,j2,j3,j4]
    mat = np.array(([i1,j1,h1],[i2,j2,h2],[i3,j3,h3],[i4,j4,h4]))
    mmin = min(h1,h2,h3,h4)
    next = np.where(mat[:,2]==mmin)
    index = next[0][0]
    return i[index] , j[index]

#--------main code

tree = ET.parse('SampleRoom.xml')
rows = tree.findall('row')
Map = []
    
for row in rows:
    cells = []
    for cell in row:
        cells.append(cell.text)
    Map.append(cells)  


 
total_rows = len(Map)
total_columns = len(Map[0])

Scan = copy.deepcopy(Map)
root = Tk()
t = Table(root)

root.update()
time.sleep(2.5)
ist,jst = index_2d(Scan,'robot')

ibat,jbat = index_2d(Scan,'Battery')

for i in range(total_rows):
    for j in range(total_columns):
        Scan[i][j] = 'blind'
        if Map[i][j] =='robot':
            Scan[i][j] = 'robot'

t = Table(root)
root.update()



test = 5;
cond = True
while cond:
    ist,jst = index_2d(Scan,'robot')
    inxt = ist
    jnxt = jst
    iend = ist
    jend = jst
    while Scan[iend][jend]!='blind':
        iend = random.randint(0,total_rows-1)
        jend = random.randint(0,total_columns-1)
    #iend = ibat
    #jend = jbat
    H = find_dist(iend,jend,total_rows,total_columns)
    while (inxt != iend) or (jend!=jnxt):
        time.sleep(0.2)
        ist,jst = index_2d(Scan,'robot')
        inxt,jnxt = find_next(ist,jst,H,Scan,Map)
        mov(ist,jst,inxt,jnxt,Map,Scan)
        if (inxt == ibat) and (jbat ==jnxt):
            inxt = iend
            jnxt = jend
            cond = False
        if Scan[max(iend-1,0)][jend] == 'obstacle' and Scan[min(iend+1,total_rows-1)][jend] == 'obstacle' and Scan[iend][max(jend-1,0)] == 'obstacle' and Scan[iend][min(jend+1,total_columns-1)]=='obstacle':
            inxt = iend
            jnxt = jend
            if iend == ibat and jend ==  jbat:
                cond = False
        H[ist,jst]=H[inxt,jnxt]+1
        if Scan[inxt][jnxt] =='obstacle':
            H[inxt,jnxt] = 1000
        t = Table(root)
        root.update()

time.sleep(1)
test = 4


test = 0
