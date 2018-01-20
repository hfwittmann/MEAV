#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:31:26 2018

@author: hfwittmann
"""

from unittest import TestCase
from MEAV import ValueTable

import numpy as np

class TestValue(TestCase):
    
    V = ValueTable()
    
    def test_basic(self):                
        self.assertIsNotNone(self.V.table, 'Table should be initiated')
        
        return None
        
    def test_set_get(self):  
        
        state = [1,2,3]
        value = 1
        
        self.V.set(state, value)        
        self.assertEqual(self.V.get(state), value)
                
        return None
    
    def test_load(self):
        
        directory = 'cache'
        fileName = 'Blubber-file-name'
        
        self.assertTrue(self.V.save(directory, fileName), 'Save should return true')
        self.assertEqual(self.V.load(directory, fileName), self.V.table)
                       
        return None
    
    def test_load_error(self):
        
        directory = 'cache'
        fileName = 'Non-existing filename'
        
        with self.assertWarns(Warning) as context0:
            self.V.load(directory, fileName)
                
        self.assertTrue('No cache found' in str(context0.warning), 'Should issue warning and continue')
        
        return None

    
    def test_setMultipleValues(self):
        
        state0 = [2,3,4]
        state1 = [3,4,5]
        value0 = 0.7
        value1 = 0.45
        
        newStates = [state0, state1]
        newValues = [value0, value1]
        
        self.V.setMultipleValues(newStates, newValues)
        self.assertEqual(self.V.get(state0),  value0, 'Should have been assigned using multiassign')
        self.assertEqual(self.V.get(state1),  value1, 'Should have been assigned using multiassign')
                
        return None
        
    #    def test_fit(self):
    #        return None
    
    def test_getMultipleValues(self):
        
        state0 = [22,32,42]
        state1 = [3,4,5]
        value0 = 0.7
        value1 = 0.45
        
        newStates = [state0, state1]
        newValues = [value0, value1]

        self.V.setMultipleValues(newStates, newValues)
        
        self.assertTrue((self.V.getMultipleValues(newStates) == newValues).all(), 'Should have been set previously')
        
        return None
    
    def test_probs(self):
        
        probsPre = [[1, 0, 0],
                 [1, 1, 0],
                 [1, 1, 1]]
        
        probs = np.array(probsPre)
        probs = probs / probs.sum()
        
        state = np.array ([1,2,3])
        
        self.V.table = {}
        
        self.assertTrue((self.V.probs(state) == probs).all(), 'The probabilites should match')
        
        return None
    
    def test_delete(self):
                
        state = [11,12,13]
        value = 1
        
        defaultValue = 0.5 #  for states that are not defined
        
        self.V.set(state, value)        
        self.assertEqual(self.V.get(state), value, 'Should have been set')

        self.V.delete(state)
        self.assertEqual(self.V.get(state), defaultValue, 'Should have been deleted')
                
        return None
    
    
#  for simple debugging self = TestValue()