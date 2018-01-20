#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:43:27 2018

@author: hfwittmann
"""
import numpy as np

# objective tests
from nim_perfect_play.nim_perfect_play import findWinningMove



class PerfectTest:
    
    def __init__(self, maxHeapSize = 7, nofPositions = 1000):
        
        # config
        maxHeapSize = maxHeapSize
        shape = [nofPositions, 3]
        
        # np.random.seed(167)
        # positions
        random_positions = np.random.randint(1,maxHeapSize+1, size = shape)

        # intialize
        next_positions = np.zeros(shape = shape)
        winning_from_random = np.zeros(shape[0], dtype = bool )
        winning_from_next = np.zeros(shape[0], dtype = bool )
        move_from_random = np.zeros([shape[0], 2])
        move_from_next = np.zeros([shape[0], 2])
        
        for heapIndex in np.arange(len(random_positions)):
        
            #  to debug    
            #    heapIndex = 0
        
            heap = random_positions[heapIndex]
            
            fWM = findWinningMove(heap)
            fWM_next = findWinningMove(fWM['next_position'])
        
            next_positions[heapIndex] = fWM['next_position']
            
            winning_from_random[heapIndex] = fWM['winning']
            move_from_random[heapIndex] = fWM['move']
        
            winning_from_next[heapIndex] = fWM_next['winning']
            move_from_next[heapIndex] = fWM_next['move']
            
        
        # https://stackoverflow.com/questions/5347065/interweaving-two-numpy-arrays
        # https://stackoverflow.com/questions/9027862/what-does-listxy-do
        positions = np.empty(shape = [ shape[0] * 2, shape[1] ])
        positions[0::2,:] = random_positions
        positions[1::2,:] = next_positions
        
        winning = np.empty(shape = shape[0] * 2)
        winning[0::2] = winning_from_random
        winning[1::2] = winning_from_next
        
        move = np.zeros([shape[0] * 2 , 2])
        move[0::2] = move_from_random
        move[1::2] = move_from_next
        
        inSample_percentage = 0.95 # 90%
        inSample = int (len(positions) * inSample_percentage)
        
        positions_InSample = positions[:inSample]
        positions_OutOfSample = positions[inSample:]
        
        winning_InSample = winning[:inSample]
        winning_OutOfSample = winning[inSample:]
        
        move_InSample = move[:inSample]
        move_OutOfSample = move[inSample:]
        
        
        self.positions = positions
        self.positions_InSample = positions_InSample
        self.positions_OutOfSample = positions_OutOfSample
        
        self.winning = winning
        self.winning_InSample = winning_InSample
        self.winning_OutOfSample = winning_OutOfSample
        
        self.move = move
        self.move_InSample = move_InSample
        self.move_OutOfSample = move_OutOfSample
        
        
        
        
        
        
        