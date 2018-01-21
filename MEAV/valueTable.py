#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:56:48 2018

@author: hfwittmann
"""

import pickle
import numpy as np

import os
import warnings
from numba import jit

class ValueTable:
    
    def __init__(self):
        
        self.table = {}
        
        return None
        
    
    def save(self, directory, name):
        
        
        directory_relative = os.path.relpath(directory)
        
        if not os.path.exists(directory_relative):
            os.makedirs(directory_relative)            
            warnings.warn (message = 'Created directory:' + directory_relative)
            
        filepath = os.path.join(directory_relative, name + ".pickle")     
        filename = open(filepath,"wb")
        
        try:    
            pickle.dump(self.table , filename)
            filename.close()
            return(True)
        except:
            return(False)
    
    def load(self, directory, name):
        
        directory_relative = os.path.relpath(directory)
        
        filepath = os.path.join(directory_relative, name + '.pickle')  
        
        try:
            
            filename = open(filepath,"rb")
            
            if filename:
                obj = pickle.load(filename)
                filename.close()

        except:
            
            warnings.warn(message='No cache found')
            obj = {}
            
            
        self.table = obj
        return(obj)
        
        
    def set(self, state, value):
        
        state_key = self._2key(state)
        
#        if state_key not in self.table:
        self.table[state_key] = value
        return value
#        else:
#            return 'Key exists in table already. Value was not changed'
        
    
    # @jit

    def setMultipleValues(self, states, values):
        # https://stackoverflow.com/questions/21222506/multiple-assignments-into-a-python-dictionary
        
        for (s,v) in zip(states, values):
            self.set (s, v)
    
    # alias
    multiassign = setMultipleValues
    
    def get(self, state):
        
        state_key = self._2key(state)
        
        if state_key in self.table:
            return self.table[state_key]
        else:
            return 0.5
    #            return float('nan')


    def fit(self, memory, gamma=0.99, alpha = 0.5, epochs=1):
            
            records = memory.replay()
            
            state = np.array(records['state'])
            
            next_state = np.array(records['next_state'])
            reward = np.array(records['reward'])
            done = np.array(records['done'])    
            
            #        targetValue = np.zeros(len(state)) # initialise
            #        
            #        #  initialise
            #        t = 0
            ##        
            #        for key in reversed(range(len(state))):
            #                    
            #            # (possibleTarget>currentValue)* possibleTarget + \
            #            #         (possibleTarget<=currentValue)* currentValue
            #            
            #            
            #            # update if continuation is at least as good
            #            # target = 1 - gamma * self.model.predict(next_state).reshape(-1)
            ##            target = 1 - gamma * self._getChildTargets(state)
            #            
            #            
            #            t = int(findWinningMove(state[key])['winning']) # Helicopter backup!!!!            
            #            # t =  gamma * (1 - t)
            #
            #            targetValue[key] = t
                
                
            for e in range(epochs):
                
                currentValue = self.predict(state).reshape(-1)    
                
                        
                # (possibleTarget>currentValue)* possibleTarget + \
                #         (possibleTarget<=currentValue)* currentValue
                
                
                # update if continuation is at least as good
                targetValue = 1 - gamma * self.predict(next_state).reshape(-1)
                # targetValue = 1 - gamma * self._getChildTargets(state)
                
                # the minus sign is due to the neutral nature of the game. 
                # Because the game is neutral, we can use the same evaluation for white and black, 
                # but must switch signs. If the evaluation for a (position, side to move) 
                # is -1 for white it is +1 for black
                # The evaluation for the same position, but with the other side to move
                # ie (position, other side to move) is 1 for white and  it is -1 for black.
                
                        
                # move currentValue gently towards target
                updatedValue = (1 - alpha) * currentValue + alpha * gamma * targetValue
                
                # set_trace()
                updatedValue[done] = reward[done] 
                # if done (ie terminated after this action) then there is only the (immediate) reward
                
                
                self.multiassign(state, updatedValue)

    

    def getMultipleValues(self, positions):
        
        multipleValues = np.zeros(len(positions))
        
        for key in range(len(positions)):
            
            multipleValues[key] = self.get(positions[key])
            

        return multipleValues            
        
    # alias
    predict = getMultipleValues
    
    # implement epsilon-greedy strategy
    def probs(self, state, epsilon=0.05):
        
        predicted_values = self._getChildPredictedValues(heaps = state)
        
        # logical not for matrix
        n_of_non_nans= np.sum(np.sum(np.sum(~ np.isnan(predicted_values))))

        #         # mask the nan values
        #         # https://stackoverflow.com/questions/37749900/how-to-disregard-the-nan-data-point-in-numpy-array-and-generate-the-normalized-d
        #         predicted_values = np.ma.array(predicted_values, mask=np.isnan(predicted_values))

        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.nan_to_num.html
        
        
        # set_trace()
        
        # is ~ one for the max-value of predicted_values, othewise zero
        # np.nanmin !!! because after the move it's the opponent's turn. And it's a zero sum game
        minPositions = (predicted_values == np.nanmin(predicted_values)) + 0 * predicted_values # to preserve nans
        
        # spread ~ 1 over the number of maxpositions
        minPositionsSpread =  minPositions / np.nansum(minPositions)
        
        # reduce by epsilon
        out = (1 - epsilon) * minPositionsSpread

        # spread epsilon over all non_nans
        out += epsilon / n_of_non_nans
        
        out_nans_are_zero = np.nan_to_num(out)
        
        return out_nans_are_zero


    def delete(self, state):
        
        state_key = self._2key(state)
        
        del self.table[state_key]
        
        
    def _getChildPredictedValues(self, heaps):
        
        # heaps is the vector of heapsizes 
        
        biggestHeap = max(heaps)
        numberOfHeaps = len(heaps)

        # first choose heap with non-zero size
        nonZeroHeaps = np.arange(numberOfHeaps) [heaps != 0]

        # zero indexed beans numbers
        predicted_values = np.zeros([numberOfHeaps, biggestHeap]) * np.nan
        
        # zero indexed
        for heapnumber in nonZeroHeaps:

            # size of the chosen heap
            heapsize = heaps[heapnumber]

            # cycle through all possible number of beans (that can be taken)
            for beansnumber in np.arange(1, heapsize + 1):

                # heaps after taken beans
                newheaps = heaps.copy() # initialise
                newheaps[heapnumber] += - beansnumber
                
                # set_trace()
                beansnumerIndex = beansnumber-1 # zero-indexed
                
                newheaps = newheaps.reshape(1,-1)
                
                predicted_values[heapnumber][beansnumerIndex] = self.predict(newheaps)
        
    
        return predicted_values
    
    
    def _2key(self, stateIn):
        
        state = np.array(stateIn, dtype=int)
        state.sort() # to reduce number of states
        return '-'.join(map(str, state))
    

#VT = ValueTable()
#
#state = [1,2,5]
#
#
#VT.set(state, 25)
#VT.delete(state)
#VT.set(state, 25)

