# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 01:51:41 2022

@author: siddharth
"""
import threading
from node import Node

class ProducerThread(threading.Thread):
    def __init__(self, id, inMemoryQueueProcessor, messageList):
        super(ProducerThread,self).__init__()
        self.id = id
        self.inMemoryQueueProcessor = inMemoryQueueProcessor
        self.messageList = messageList
      

    def run(self):
        for message,ttl in self.messageList:
            retry = 3
            while(retry > 0):
                try:
                    self.inMemoryQueueProcessor.publishMessage(message,ttl)
                    break
                except Exception as e:
                    print(e)
                    retry = retry - 1
            if retry == 0:
                self.inMemoryQueueProcessor.addMesageToDeadLetterQueue(message,ttl)
        return
        