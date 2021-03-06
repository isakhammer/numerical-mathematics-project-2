#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 19:09:31 2020

@author: isakh
"""
import numpy as np
import os

def generate_synthetic_batches(I,func = "2sqr"):
    
    batch = {} 
    
    if func == "2sqr":
        
        d_0 = 2
        """
        Y1 = np.linspace(-1,1,I)
        Y2 = np.linspace(1,-1,I)
    
        batch["Y"] = np.array([Y1,Y2])
        batch["Y"] = np.array([[1,1],
                              [1,2]])
        """
        
        batch["Y"] = np.random.uniform(high=2, low=-2, size=(d_0,I) )    
    
    
        batch["c"] = 0.5*batch["Y"][0,:]**2 + 0.5*batch["Y"][1,:]**2
        batch["c"] = batch["c"][:, np.newaxis]
        
        return batch
    
    elif func == "1sqr":
        d_0 = 1
        
        batch["Y"] = np.random.uniform(high=2, low=-2, size=(d_0,I) )
        batch["c"] = 0.5*(batch["Y"])**2
        batch["c"] = batch["c"].T
        
        return batch
    
    elif func == "1cos":
        d_0 = 1
        
        batch["Y"] = np.random.uniform(high=np.pi/3, low=-np.pi/3, size=(d_0,I) )
        batch["c"] = 1 - np.cos(batch["Y"])
        batch["c"] = batch["c"].T
        
        return batch
    
    elif func == "2norm-1":
        d_0 = 2
        
        if I%2 == 1:
            raise Exception("I not even")
            
            
        Y = np.random.uniform(high=2, low=-2, size=(d_0,I))
        
        signs = np.array([-1,1])
        indexes = np.array([0,1])
        
        for i in range(I):
            y = Y[:,i]
            
            if np.linalg.norm(y) < 1/4:
                j = np.random.choice(indexes)
                sign = np.random.choice(signs)
                Y[j,i] = Y[j,i] + sign*(1/2)
            
            
        """    
        signs = np.array([-1,1])
        Y = np.random.uniform(high=2, low=1/4, size=(d_0,I))
        
        for i in range(d_0):
            for j in range(I):
                sign = np.random.choice(signs)
                Y[i,j] = sign*Y[i,j]
        """         
        
            
        """
        Y1 = np.random.uniform(high=2, low=1/4, size=(d_0,int(I/2)))
        Y2 = np.random.uniform(high=-1/4, low=-2, size=(d_0,int(I/2)))
        Y = np.append(Y1,Y2,1)
        np.random.shuffle(Y)
        """
        batch["Y"] = Y
        
        
        batch["c"] = -1/np.sqrt(batch["Y"][0]**2 + batch["Y"][1]**2)
        batch["c"] = batch["c"].T
        batch["c"] = batch["c"][:, np.newaxis]
            
        return batch
        
    
    else:
        raise Exception("Not axeped func")
        
        
def import_batches():
    n_batches = 49
    
    data_prefix = "datalist_batch_"
    data_path = os.path.join(os.path.dirname(__file__), "project_2_trajectories")
    
    batches = {}
    
    for i in range(n_batches):
        # assemble track import path
        batch_path = os.path.join(data_path, data_prefix + str(i) + ".csv")
        batch_data = np.loadtxt(batch_path, delimiter=',', skiprows=1)
        
        # np.newaxis is adding a dimension such that (I,) -> (I, 1)
        batch = {}
        batch["t"] = batch_data[:, 0, np.newaxis]
        batch["Y_q"] = batch_data[:, 1:4].T
        batch["Y_p"] = batch_data[:, 4:7].T
        batch["c_p"] = batch_data[:, 7, np.newaxis] 
        batch["c_q"] = batch_data[:, 8, np.newaxis] # potential energy
        
        batches[i] = batch

    return batches

def import_one_batch():
   
    data_prefix = "datalist_batch_"
    data_path = os.path.join(os.path.dirname(__file__), "project_2_trajectories")
    
    batches = {}
    
    i = 0
    # assemble track import path
    batch_path = os.path.join(data_path, data_prefix + str(i) + ".csv")
    batch_data = np.loadtxt(batch_path, delimiter=',', skiprows=1)
        
    # np.newaxis is adding a dimension such that (I,) -> (I, 1)
    batch = {}
    batch["t"] = batch_data[:, 0, np.newaxis]
    batch["Y_q"] = batch_data[:, 1:4].T
    batch["Y_p"] = batch_data[:, 4:7].T
    batch["c_p"] = batch_data[:, 7, np.newaxis] 
    batch["c_q"] = batch_data[:, 8, np.newaxis] # potential energy
        
    batches[0] = batch

    return batch
    
        
        
        
        
        
