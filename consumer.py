# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 00:06:25 2022

@author: siddharth
"""

from node import Node

class Consumer:
    def __init__(self, externalConsumer, id, pattern, dependencyList, deadLetterQueue):
        self.externalConsumer = externalConsumer
        self.id = id
        self.messagePattern = pattern
        self.dependencyList = dependencyList
        self.deadLetterQueue = deadLetterQueue
        
    def getId(self):
        return self.id
    
    def getMessageRegexPattern(self):
        return self.messagePattern
    
    def checkIfMessagePatternExist(self):
        if self.messagePattern:
            return True
        return False
    
    def sendMessage(self, message, ttl):
        retry = 3
        while(retry > 0):
            try:
                self.externalConsumer.process(message)
                break
            except Exception as e:
                print(e)
                retry = retry - 1
        if retry == 0:
            messageNode = Node(message,ttl)
            self.deadLetterQueue.enqueue(messageNode)
            
        
    def getDependentConsumer(self):
        return self.dependencyList