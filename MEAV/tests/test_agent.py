#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:42:10 2018

@author: hfwittmann
"""

class mockedEnvironment:
    def __init__(self):
        self.state = {}
        return None
    
class mockedValueTable:
    def __init__(self):
        return None

from unittest import TestCase
from MEAV import Agent

import numpy as np

class TestAgent(TestCase):
    
    def test_basic(self):
        
        self.assertEqual(1,1)
        
        A = Agent()
        E = mockedEnvironment()
        V = mockedValueTable()      
        
        
        def mockedProbs0(state, epsilon=0.02):            
            return np.array(
                            [[0  , 0   , 1000],
                             [0.25, 0.125, 0.125],
                             [0.125, 0, 0]]
                             )
        # the probability table is normalised to 1, therefore 1000 is 
        # chosen with a high probability
        
        
        def mockedProbs1(state, epsilon=0.02):            
            return np.array(
                            [[0  , 1   , 0],
                             [0 , 0 , 0],
                             [0 , 0 , 0]]
                             )
        
        def mockedProbs2(state, epsilon=0.02):            
            return np.array(
                            [[0  , 0   , 0],
                             [0 , 0 , 1],
                             [0 , 0 , 0]]
                             )
            
        def mockedProbs3(state, epsilon=0.02):            
            return np.array(
                            [[0  , 0   , 0],
                             [0 , 0 , 0],
                             [1 , 0 , 0]]
                             )
        
        
        
        np.random.seed(167)
        # mock probs for V
        V.probs = mockedProbs0
        
        action, diffs_prob_chosen_max, probs = A.chooseAction(E, V)
        self.assertEqual( [0, 3], action, \
                         "Should have chosen to take three from the zero-th heap")
        self.assertEqual(0, diffs_prob_chosen_max, \
                         "Should have chosen action with maximum probability")
        
        # Overwrite prob for mocking
        V.probs = mockedProbs1
        
        action, diffs_prob_chosen_max, probs = A.chooseAction(E, V)
        self.assertEqual( [0, 2], action, \
                         "Should have chosen to take two from the zero-th heap")
        self.assertEqual(0, diffs_prob_chosen_max, \
                         "Should have chosen action with maximum probability")

        # Overwrite prob for mocking
        V.probs = mockedProbs2
        
        action, diffs_prob_chosen_max, probs = A.chooseAction(E, V)
        self.assertEqual( [1, 3], action, \
                         "Should have chosen to take three from the one-th heap")
        self.assertEqual(0, diffs_prob_chosen_max, \
                         "Should have chosen action with maximum probability")

        # Overwrite prob for mocking
        V.probs = mockedProbs3
        
        action, diffs_prob_chosen_max, probs = A.chooseAction(E, V)
        self.assertEqual( [2, 1], action, \
                         "Should have chosen to take three from the two-th heap")
        self.assertEqual(0, diffs_prob_chosen_max, \
                         "Should have chosen action with maximum probability")

        
# for simple debugging : self = TestAgent()
                         