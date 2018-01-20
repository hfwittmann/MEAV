#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 17:34:11 2018

@author: hfwittmann
"""

import numpy as np

class mockedMemory:
    def __init__(self, capacity):    
        return None
    
    def replay(self):
        
        out = {}
        out['action'] = [[0,1]]
        
        return out
    
class mockedEnvironment:
    def __init__(self, maxHeapSize = 7):    
        return None
    
    def reset(self, heaps=None, value=None):
        return None
    
    def act(self, action, memory, save2Memory=True):
        
        reward = 1
        done = True
        
        return 'next_state', reward, done, '_'
        

class mockedAgent:
    def __init__(self):    
        return None
    
    def chooseAction(self, environment, value, epsilon=0.05):
        return (0, 2), np.array([]), np.array([])
    
    
class mockedValue:
    def __init__(self):
        
        self.table = {}
        return None

    def save(self, directory, name):
        return None

    def load(self, directory, name):
        return None
    
    def fit(self, memory, gamma=0.99, alpha=0.5, epochs=1):
        return None
    
    def predict(self, positions):
    
        winningNess = np.array([1,1,0])
        
        return winningNess
    
    
class mockedPerfectTest:
    def __init__(self):
        
        self.positions = np.array([[1,1,1],[7,5,1],[0,1,1]])
        self.winning = np.array([1,1,1])
        return None
    
        
    
from unittest import TestCase
from MEAV import RunOnPolicy

class TestRunOnPolicy(TestCase):

    M = mockedMemory
    E = mockedEnvironment
    A = mockedAgent
    V = mockedValue
    
    P = mockedPerfectTest
    
    rOP = RunOnPolicy(M, E, A, V, P)
    
    def test_basic(self):
    
        accuracy_predictions, tableSize, memorySize,reward, \
            stats_rewards, stats_difference_prob_chosen_max, stats_accuracy = self.rOP.runEpisodes()
        
        self.assertEqual(accuracy_predictions, 2/3, \
                         "Should be two thirds, as \
                         winningNess = np.array([1,1,0]) in mockedValue and \
                         self.winning = np.array([1,1,1]) in mockedPerfectTest \
                         ")
        
        return None
    
        
        
# for easy debugging: self = TestRunOnPolicy()
        
        
        
        
        
        
        
        
        
        
        
        
        
        