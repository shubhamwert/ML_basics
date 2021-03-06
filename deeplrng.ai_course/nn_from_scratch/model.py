import numpy as np
import matplotlib.pyplot as plt

class NN_1_layer:
    def __init__(self,input_features_size,output_size,lr_start=0.01):
        self.input_features_size=input_features_size
        self.h_size=10
        self.weights1=np.random.rand(self.h_size,self.input_features_size)
        self.output_size=output_size
        self.weights2=np.random.rand(self.output_size,self.h_size)*0.01
        self.bias1=np.zeros([self.h_size,1])
        self.bias2=np.zeros([self.output_size,1])
        self.lr=lr_start
    def sigmoid(self,X):
        temp=np.exp(-X)
        return 1/(1+temp)

    

    def forward(self,X):
        Z1=np.dot(X,self.weights1.T)+self.bias1.T
        a1=self.sigmoid(Z1)
        Z2=np.dot(a1,self.weights2.T)+self.bias2.T
        a2=self.sigmoid(Z2)
        return a2,a1
    
    def error(self,X,y):
        y_hat=self.forward(X)[0]
        assert(y_hat.shape==y.shape)
        # error=np.sum(np.sum(y*np.log(y_hat))+np.sum((1-y)*np.log(1-y_hat)))/y.shape[0]
        error=np.power(np.sum(np.power(y-y_hat,2)),1/2)/y.shape[0]
        return error
    # def score(self,X,y):
    #     y_hat=self.forward(X)[0]
    #     p=[1 if k>0.5 else 0 for k in y_hat[0]]
    #     print(p)
    #     return np.array(p)
    def backward_propogation(self,X,y):
        m=X.shape[0]
        a2,a1=self.forward(X)

        dZ2=a2-y
        dW2=((dZ2.T.dot(a1))/m)
        
        assert(dW2.shape==self.weights2.shape)
        db2 = np.sum(dZ2.T,axis=1,keepdims=True)/m
        # print(dW2.shape)
        # print(dZ2.shape)
        # print(a1.shape)

        dZ1 = 2*(dZ2.dot(dW2))*a1*(1-a1)
        dW1 = (dZ1.T.dot(X))/m
        assert(dW1.shape==self.weights1.shape)
        db1 = np.sum(dZ1.T,axis=1,keepdims=True)/m
        self.update_weights(dW2,db2,dW1,db1)
    def update_weights(self,dW2,db2,dW1,db1):
        self.weights1=self.weights1-self.lr*dW1
        self.weights2=self.weights2-self.lr*dW2
        self.bias1=self.bias1-self.lr*db1
        self.bias2=self.bias2-self.lr*db2

    def fit(self,X,y,num_iters=1000):
        for i in range(0,num_iters):
            self.backward_propogation(X,y)

            cost=self.error(X,y)

            if i % 100 == 0:
                print ("Cost after iteration %i: %f" %(i, cost))

    def predict(self,X):
        a2,a1=self.forward(X)
        return a2