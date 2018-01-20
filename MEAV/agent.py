#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:19:04 2018

@author: hfwittmann
"""

import numpy as np

class Agent:
    
    def __init_(self):
        
        return None
    
    def chooseAction(self, environment, value, epsilon=0.05):      

        probs = value.probs(environment.state, epsilon=epsilon)
        probs = probs / probs.sum()
        
        # print('probs:', probs)
        # set_trace()
        probs_1_dim = probs.reshape([-1])
        
        action_pre = np.random.choice(np.prod(probs.shape), p = probs_1_dim)

        diffs_prob_chosen_max = probs_1_dim[action_pre] - np.max(probs_1_dim)
        
        heapindex = action_pre//probs.shape[1] # zero-indexed
        beansindex = action_pre%probs.shape[1] # zero-indexed
        beansnumber = beansindex + 1
        
        action = [heapindex, beansnumber] 
        
        # print( action_pre, action)
        
        return action, diffs_prob_chosen_max, probs