#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 23:16:55 2018

@author: hfwittmann
"""

class mockedAction:
    
    def __init__(self):
        return None
    
    def chooseAction(self): 
        return [0, 1]
    
class mockedMemory:
    
    def __init__(self):
        return None

    def saveRecord(self, Record):
        return None


from unittest import TestCase
from MEAV import Environment

class TestEnvironment(TestCase):

    E = Environment()
        
    def test_basic(self):
        
        self.assertEqual(self.E.env.MaxHeapSize, 7) 
        return None
    
    def test_reset(self):

        self.E.reset()
        self.assertFalse(self.E.done,"Should not be finished straight after reset")
        
        return None
    
    def test_act(self):
        
        A = mockedAction()
        M = mockedMemory()

        action = A.chooseAction()        
        
        state =  self.E.env.state.copy()
        
        
        self.E.act(action, M)
        
        previous_state = self.E.previous_state.copy()
        
        
        self.assertTrue ((state == previous_state).all(), \
                         "The previous current state should be the new previous state")
        
        
        return None
        

# for simple debugging: self = TestEnvironment() 