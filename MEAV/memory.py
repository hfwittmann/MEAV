#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:20:02 2018

@author: hfwittmann
"""

class Memory:
    
    def __init__(self, capacity):
        # capacity : how much memory can the class hold?
        self.capacity = capacity
        
        self.clear()

        return None
    
    def saveRecord( self, thisRecord):
        
        records = self.__records.copy()
        
        for key in thisRecord.keys():
            
            records[key].append(thisRecord[key])
            
            # if no more capacity then clean out the oldest records
            if len(records[key])>self.capacity:
                records[key].pop(0)
                
        self.__records = records.copy()
            
        return None
    
    def replay(self):
        
        return self.__records
    
    def clear(self):
        
        self.__records = {}
        self.__records['state'] = []
        self.__records['action'] = []
        self.__records['next_state'] = []
        self.__records['reward'] = []
        self.__records['done'] = []
        
        return None