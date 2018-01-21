#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:22:17 2018

@author: hfwittmann
"""

import sys
import numpy as np

class RunOnPolicy:
    
    def __init__(self, Memory, Environment, Agent, Value, Accuracy, maxHeapSize = 7, numberOfHeaps = 3):
        
        self.environment = Environment(maxHeapSize=maxHeapSize,numberOfHeaps=numberOfHeaps)
        self.value = Value()
        self.value.load('cache', 'mytable-nim')
        
        self.agent = Agent()
        self.memory = Memory(capacity = 1000)
        
        # objective out of sample test
        self.Accuracy = Accuracy(maxHeapSize=maxHeapSize, numberOfHeaps=numberOfHeaps)
        
        return None
    
    
    def runEpisodes(self, maxCount=5000, desired_accuracy_predictions=0.98):
        
        # initialise
        count = 0
        
        accuracy_predictions =  0.5
        
        self.stats_difference_prob_chosen_max = []
        self.stats_accuracy=[]
        self.stats_rewards=[]
        
        while count<maxCount and \
              accuracy_predictions<desired_accuracy_predictions:
    
            count +=1
        
            totalReward = 0
            totalDifference = 0
            
            self.environment.reset()
            
            done = False
            # self.memory.clear()
                            
            # set_trace()
            
            while not done:
                
                # epsilon = np.max([0.0001, np.exp(-0.1 * count)])
                epsilon = 0.01 + np.max([0, 0.05 - count / 20000 ])
                # epsilon = 0.01 # simple but fixed
                    
                action, diffs_prob_chosen_max, probs = self.agent.chooseAction(environment = self.environment,\
                                     value = self.value,\
                                     epsilon = epsilon)

                if diffs_prob_chosen_max != 0:
                    print('diffs_prob_chosen_max:', diffs_prob_chosen_max)
                    test_i = 1
                if diffs_prob_chosen_max == 0:
                    test_i = 0
                
                # print('state:{}, action:{}'.format( self.environment.state, action))
                # set_trace()
                
                save2Memory = diffs_prob_chosen_max == 0
                
                next_state, reward, done, _ = \
                    self.environment.act(action=action, memory=self.memory, save2Memory=save2Memory)

                totalReward += reward
                totalDifference += diffs_prob_chosen_max

            
            # alpha=0.5 is faster than e.g. alpha=0.1
            self.value.fit(self.memory, gamma=1, alpha=0.5, epochs=1)            
            self.value.save('cache', 'mytable-nim')
            
            
            memorySize = len(self.memory.replay()['action'])
            
            tableSize = len(self.value.table)
            
            winning_prediction = self.value.predict(self.Accuracy.positions) > 0.5
            
            accuracy_predictions = ( self.Accuracy.winning == winning_prediction.reshape(-1)).mean()
            
            self.stats_rewards.append(totalReward)
            self.stats_difference_prob_chosen_max.append(totalDifference)
            
            self.stats_accuracy.append(accuracy_predictions)
           
            
            
            self.value.save('cache', 'accuracy-nim')
            
            print('\r accuracy_predictions {}, \
                      tableSize : {} \
                      memorySize: {}, \
                      reward :{}'.format(
                                         accuracy_predictions,\
                                         tableSize,\
                                         memorySize,\
                                         reward), end="")
            sys.stdout.flush()  
            

        return accuracy_predictions, tableSize, memorySize, reward,\
            self.stats_rewards, self.stats_difference_prob_chosen_max, self.stats_accuracy
            
            






