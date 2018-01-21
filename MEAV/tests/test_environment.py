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
        
        self.assertEqual(self.E.env.maxHeapSize, 7)
        self.assertEqual(self.E.env.numberOfHeaps, 3)
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
    
    def test_set_number_of_heaps(self):
        
        self.E.setNumberOfHeaps(4)
        self.assertEqual(self.E.env.numberOfHeaps, 4, "Number of heaps should have changed")
        
        
        
    def test_set_max_heap_size(self):
        
        self.E.setMaxHeapSize(10)
        self.assertEqual(self.E.env.maxHeapSize, 10, "Heap Size should have changed")
        
        
        
        

# for simple debugging: self = TestEnvironment() 