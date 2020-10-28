import numpy as np
from neural_net import *
from parameters import *
from data import *
import matplotlib.pyplot as plt
import sys
from functions import *

def train_net(c, Y, model_pars):
        
    # TODO: pass in dictionary as a parameter instead of variables.
    d_0 = model_pars["d_0"] 
    d       = model_pars["d"]
    K       = model_pars["K"]
    tau     = model_pars["tau"]
    bsize   = model_pars["bsize"]
    max_it  = model_pars["max_it"]
    h       = model_pars["h"]
    tau     = model_pars["tau"]
    sifts   = model_pars["sifts"]
    bsize   = model_pars["bsize"]
    max_it   = model_pars["max_it"]
    
    th = initialize_weights(d_0, d, K)
  
    JJ, th = stocgradient(c, d, d_0, K, h, Y, th, tau, sifts, bsize, max_it)
    #JJ, th = train(c, d, d_0, K, h, Y, th, tau, max_it, method="adam")
    
    return JJ, th
    


def kepler(p,q):
    if (p.shape[0] != 2) or (q.shape[0] != 2):
        print("Wrong dimension")
        sys.exit(1)
    
    K = 0.5* (p[0]**2 + p[1]**2) 
    V = -1/np.sqrt(q[0]**2 + q[1]**2) 
    
    return K, V

 
def train_model(model_pars, func):
    # Generate data
    batches = generate_batches( model_pars["I"], model_pars["n_batches"],  model_pars["d_0"], func)
    
    # Evaluate K neural net
    Y_K, c_K = merge_batches(batches["K"])
    c_K, a, b, alfa, beta = scale(c_K) # why return hundred parameters???
    JJ_K, th_K = train_net(c=c_K, Y=Y_K,  model_pars=model_pars)   
    it = np.arange(JJ_K.shape[0])
    plt.title("th_K Weights " + model_pars["weights"])
    plt.plot(it, JJ_K)
    plt.show()
    # Evaluate V neural net
    Y_V, c_V = merge_batches(batches["V"])
    c_V, a, b, alfa, beta = scale(c_V) # why return hundred parameters???
    JJ_V, th_V = train_net(c=c_V, Y=Y_V,  model_pars=model_pars)   
    it = np.arange(JJ_V.shape[0])
    plt.title("th_V Weights " + model_pars["weights"])
    plt.plot(it, JJ_V)
    plt.show()
    
    th = {}
    th["V"] = th_V
    th["K"] = th_K
    th_file = open(model_pars["weights"], "wb")
    pickle.dump(th, th_file)
    th_file.close()

    return


def train_analytic():

    # Train model 1
    kepler_pars = get_params(model="kepler")
    train_model(model_pars=kepler_pars, func=kepler)  
    return


def merge_batches(batches):
    d_0 = batches[0]["Y"].shape[0]
           
    Y = [] 
    c = []
    for i in range(len(batches)):
        batch = batches[i]
        Y.append( batch["Y"])
        c.append( batch["c"])
        
    Y = np.stack(Y).reshape( d_0,-1 )
    c = np.stack(c).reshape(-1,1)
    return Y, c

def train_uknown():
    pars = get_params(model="uknown")
    
    K = pars["K"]
    h = pars["h"]
    #I = pars["uknown"]["I"]
    
    max_it = pars["max_it"]
    tau = pars["tau"]
    
    #Y = batch1["Y_q"]

    # Import batches
    batches = import_batches()
    #batch1 = batches[0]
    antB = 10
    testbatch = batches[antB-1]
    
    bigbatch = {}
    bigbatch["Y"] = np.array([[],[],[]])
    bigbatch["c"] = np.array([])
    
    for i in range(antB):
        batch = batches[i]
        bigbatch["Y"] = np.append(bigbatch["Y"],batch["Y_q"],1)
        bigbatch["c"] = np.append(bigbatch["c"],batch["c_q"])
        
    Y = bigbatch["Y"]
    c,a,b,alfa,beta = scale(bigbatch["c"][:,np.newaxis])
    
    # Train net
    JJ, th = train_net(c, Y, model_pars=pars)
        
    plt.plot(JJ)
    plt.yscale("log")
    plt.show()
    
    tY = testbatch["Y_q"]
    tc,a,b,alfa,beta = scale(testbatch["c_q"])
    z, yhat = F_tilde(tY, th, d_0, pars["d"], pars["K"], pars["h"])
    
    #y = invscale(yhat, a, b, alpha, beta) 
    
    plt.plot(yhat)
    plt.plot(tc)
    plt.show()
    
    th_file = open(pars["weights_file"], "wb")
    pickle.dump(th, th_file)
    th_file.close()

    return

#train_uknown()
train_analytic()