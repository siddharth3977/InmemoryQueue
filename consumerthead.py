# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 02:32:52 2022

@author: siddharth
"""

from time import sleep


import threading

class ConsumerThread(threading.Thread):
    def __init__(self, id):
        super(ConsumerThread,self).__init__()
        self.id = id
        self.messageList = []
      

    def run(self):
        pass
    
    def process(self, message):
        print("consumer - "+ str(self.id) + "---processing message --- " + str(message))
        self.messageList.append(message)
      