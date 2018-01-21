#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 15:09:30 2018

@author: hfwittmann
"""

from unittest import TestCase

from MEAV import Accuracy


class TestAccuracy(TestCase):
    
    
    def test_basic(self):
                
        maxHeapSize = 5
        numberOfHeaps = 4
        nofPositions = 100        
        
        A = Accuracy(maxHeapSize = maxHeapSize, \
                     numberOfHeaps = numberOfHeaps,\
                     nofPositions = nofPositions)
        
        self.assertEqual(A.positions.shape, (2 * nofPositions, numberOfHeaps), "Number of positions and heaps")
        self.assertEqual(A.winning.shape, (2 * nofPositions, ) , "Number of positions")        
        self.assertEqual(A.move.shape, (2 * nofPositions, 2 ), "Number of positions, 2")            
    
    
    
# for easy debugging self = TestAccuracy()