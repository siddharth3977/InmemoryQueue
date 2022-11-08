# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:25:01 2022

@author: siddharth
"""

from node import Node
from concurrent.futures import ThreadPoolExecutor
import re
import time
from consumer import Consumer
from inmemoryqueue import InMemoryQueue
from cycledetector import CycleDetector


class InMemoryQueueProcessor:
    def __init__(self, inMemoryQueue, workers):
        self.inMemoryQueue = inMemoryQueue
        self.workers = workers
        self.consumerList = []
        self.threadPoolExecutor = ThreadPoolExecutor(workers)
        self.submittedTask = []
        self.consumerMap = {}
        self.subscriptionMap = {}
        self.deadLetterQueue = InMemoryQueue(1000)
        
            
    def publishMessage(self, message, ttl=0):
        messageNode = Node(message,ttl)
        self.inMemoryQueue.enqueue(messageNode)
        print("message added "+ str(message))
        futuretask = self.threadPoolExecutor.submit(self.sendMessageToConsumer)
        self.submittedTask.append(futuretask)
    
    def registerConsumer(self, consumer, id, pattern, dependecyList):
        consumerObj = Consumer(consumer, id, pattern, dependecyList, self.deadLetterQueue)
        self.subscriptionMap[id] = dependecyList
        self.checkCyclicDependency(id)
        self.consumerList.append(consumerObj)
        self.consumerMap[id] = consumerObj
        
        
        
    def sendMessageToConsumer(self):
        #print("going to consume")
        message, ttl = self.inMemoryQueue.dequeue()
        if self.isMessageAlive(ttl):
            messageString = str(message)
            sentList = []
            for consumer in self.consumerList:
                if consumer.getId() in sentList:
                    continue
                if self.checkSubscriptions(consumer, messageString):
                    dependentConsumersList = consumer.getDependentConsumer()
                    for dependentConsumer in dependentConsumersList:
                        if dependentConsumer in sentList:
                            continue
                        dependentConsumerObj = self.consumerMap[dependentConsumer]
                        self.sendMessage(dependentConsumerObj, message, ttl)
                        sentList.append(dependentConsumerObj.getId())
                    self.sendMessage(consumer, message, ttl)
                    sentList.append(consumer.getId())
                    
    
    def sendMessage(self, consumer, message, ttl):
        consumer.sendMessage(message, ttl)
        
    
                
    def checkCyclicDependency(self, id):   
        cycleDetector = CycleDetector()
        if not cycleDetector.checkCyclicDependency(self.subscriptionMap):
            raise Exception("cyclic dependency")
                    

    def completeAllTask(self):
        for task in self.submittedTask:
            task.result()
     
    def isMessageAlive(self, ttl):
        if ttl == 0:
            return True
        curr_time = round(time.time()*1000)
        if curr_time > ttl:
            return False
        return True
        
        
    def checkSubscriptions(self, consumer, messageString):
        if consumer.checkIfMessagePatternExist():
            regexp = re.compile(consumer.getMessageRegexPattern())
            if regexp.search(messageString):
                return True
            return False
        return True
    
    def addMesageToDeadLetterQueue(self, message, ttl):
        messageNode = Node(message,ttl)
        self.deadLetterQueue.enqueue(messageNode)