#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:22:27 2020

@author: isakh
"""

"""
Stormler Vermet.

Notation:
d - dimensions of p,q
p - Generalized Coordinates
q - Conjugate momenta
V -  Potential energy function
T - Kinetic energy function

Input:
 p0: (d,1) numpy array of inital values
 q0: (d,1) numpy array of inital values
 t0: Inital time
 T:  Terminal time
 dV: Function dV(q)/dq
 dT: Function dT(p)/dp
Output:
  q: (d, N) numpy array of all values from t0,T
  p: (d, N) numpy array of all values from t0,T
  t: (1, N) numpy array for time

"""

def stormer_verlet(p0, q0, t0, T, h, dV, dT):
  
  N = int(T/h)
  p = np.zeros((p0.shape[0], N))
  q = np.zeros((q0.shape[0], N))
  t = np.zeros((1, N))

  p[0] = p0
  q[0] = q0
  t[0] = t0

  for i in range(N):
    phat = p[:,i-1] - 0.5*h*dV(q[:,i-1])
    q[:, i] = q[:, i-1] + h*dT(phat)
    p[:, i] = phat - 0.5*h*dT(q[:,i])
    t[:,i] = t[:,i-1] + h

  return p,q,t

 

def symplectic_test( function_name: str):
    # import weights th_q, th_p for this function
    # run symplectic method
    # evaluate T - V
    # plot as a function of time.
    return
    
    
    
    