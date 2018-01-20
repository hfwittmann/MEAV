#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:42:10 2018

@author: hfwittmann
"""

from unittest import TestCase
from MEAV import Memory

class TestMemory(TestCase):                      
        
 
    # allowed keys are state, next_state, action, reward, done        
    record = {}
    record['state'] = (22,23,24)
    record['next_state'] = (21,23,24)
    record['action'] = (0, 1) # take 1 from the zero-th heap
    record['reward'] = 0 # no reward
    record['done'] = False
    
    
    falseRecord = {}
    falseRecord['falseState'] = 'This key is not allowed'
    
    
    def test_basic(self):
        
        self.assertEqual(1,1, 'Numbers should be equal')
        
        #  memory capacity
        capacity = 1000
        
        M = Memory(capacity)
        
        self.assertEqual(M.capacity, capacity, 'Memory capcity should have been set')
        
    def test_saveNreplay_0(self):
 
        capacity = 7
        M = Memory(capacity)
        
        M.saveRecord(thisRecord=self.record)
        
        M_records = M.replay()
        
        #count number of records
        for key in self.record:
            print(key)
            self.assertEqual (len (M_records[key]) , 1, 'Only one saved as yet')
       

    def test_saveNreplay_1(self):
        
        capacity = 7
        M = Memory(capacity)
        
        # save more records than capacity, in fact twice as many
        for c in range(capacity * 2):    
            M.saveRecord(thisRecord=self.record)
        
        M_records = M.replay()
        
        #count number of records
        for key in self.record:
            print(key)
            self.assertEqual (len (M_records[key]) , 7, \
                'Should be capacity, as when records execeed capacity the oldest ones are discarded, using FIFO = first in first out')
        



    def test_save_failure(self):
        
        capacity = 7
        M = Memory(capacity)
        
        # prototype for assertion error test
        # https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(KeyError) as context0:
            
            # cause assertionError
                    # try to save false record to cause failure
                    M.saveRecord(self.falseRecord)
        
        # https://stackoverflow.com/questions/284043/outputting-data-from-unit-test-in-python
        self.assertTrue('falseState' in str(context0.exception), 'Should complain about wrong key : falseState')
        # end : prototype
        
        
        
    def test_clear(self):
        
        capacity = 7
        M = Memory(capacity)
        
        M.saveRecord(thisRecord=self.record)
        
        M.clear()
        
        M_records = M.replay()
        
        #count number of records
        for key in self.record:
            print(key)
            self.assertEqual (len (M_records[key]) , 0, 'Records Should have been cleared')
            
        
        
        return None
        
    

        
# for simple debugging : self = TestMemory()
                         