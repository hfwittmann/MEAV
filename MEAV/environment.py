#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:12:00 2018

@author: hfwittmann
"""

import gym
import gym_game_nim
env = gym.make('game_nim-v0')

class Environment:
    def __init__(self, maxHeapSize = 7):
        
        self.env = env
        self.env.setMaxHeapSize(maxHeapSize)
        
        self.reset()
        
        return None
    
    def reset(self, heaps = None, value = None):
        
#        # choose starting position not yet in table
#        if value:
#            done = False
#            
#            while not done:
#    
#                self.env.setHeapsStartingPositions(heaps)
#                
#                key = value._2key(self.env.heaps)
#                
#                if key not in value.table:
#                    
#                    done  = True
#        
#        # choose any starting position        
#        else:
            
        self.env.setHeapsStartingPositions(heaps)
            
        
        self.env.reset()   
        self.state = self.env.state.copy()
        self.next_state = None
        self.previous_state = None
        self.done = False
        
        return None
        
    def act(self, action, memory, save2Memory=True):
        
        self.state = env.state.copy()
        next_state, reward, done, _ = env.step(action=action)
        
        self.next_state = next_state.copy()
        
        if save2Memory:            
            memory.saveRecord({"state":self.state})
            memory.saveRecord({"action":action})
            memory.saveRecord({"next_state":self.next_state})
            memory.saveRecord({"reward":reward})
            memory.saveRecord({"done":done})
                                   
        self.previous_state = self.state.copy()
        self.state = self.next_state.copy()

        return self.next_state, reward, done, _
        
    
# environment = Environment(env)
