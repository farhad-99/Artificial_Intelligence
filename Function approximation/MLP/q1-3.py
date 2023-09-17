import numpy as np
import math
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPRegressor

sample = 100
start = 2.5
x_train = np.linspace(-start,start,sample).reshape(-1, 1)

#y_train =np.sin(x_train*math.pi)
y_train = x_train * np.sin(2*x_train) - np.cos(3*x_train) +x_train**2
max_iter_ = 2000

i = 20
j=40
k=20
hidden_layer_sizes_ = (i,j,k)

        
network = MLPRegressor( hidden_layer_sizes= hidden_layer_sizes_,
                                max_iter=max_iter_,
                                random_state=1,
                                shuffle=True)


guess_network = network.fit(x_train,y_train.ravel())

x_test = np.linspace(-10,10,5000).reshape(-1, 1)
y_test = guess_network.predict(x_test).reshape(-1, 1)
y_validation = x_test * np.sin(2*x_test) - np.cos(3*x_test) +x_test**2 
dist = (y_test - y_validation)
error = np.sum(np.abs(dist))/sample

fig, ax = plt.subplots()
train, = ax.plot(x_train,y_train, label='train')
test, = ax.plot(x_test,y_test, label='test')
valid, = ax.plot(x_test,y_validation, label='validation',linestyle='dotted')

ax.legend(handles=[train,test,valid])
plt.title('for['+str(start)+','+str(-start)+'] '+',number of samples:'+str(sample)+' & '+str(max_iter_)+'iterations the error is:'+str(round(error,3)),fontsize=10)
#plt.title('number of samples:'+str(sample)+' & '+str(max_iter_)+'iterations the error is:'+str(round(error,3)),fontsize=10)
#plt.title('number of neurons:'+str(i)+' ,number of samples:'+str(sample)+' & '+str(max_iter_)+'iterations the error is:'+str(round(error,3)),fontsize=10)
#plt.title('number of  neurons in layers :'+str(i)+','+str(j)+','+str(k)+' The error is:'+str(round(error,3)),fontsize=10)
#plt.title(' & '+str(max_iter_)+'iterations the error is:'+str(round(error,3)),fontsize=10)
plt.show()