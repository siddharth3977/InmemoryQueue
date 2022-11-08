# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 02:32:52 2022

@author: siddharth
"""

from time import sleep
from acknowledgements import Acknowledgement

import threading

class ConsumerThread(threading.Thread):
    def __init__(self, id):
        super(ConsumerThread,self).__init__()
        self.id = id
        self.messageList = []
      

    def run(self):
        
        pass
    
    def process(self, message):
        try:
            print("consumer - "+ str(self.id) + "---processing message --- " + str(message))
            self.messageList.append(message)
        except Exception as e:
            print(e)
            return Acknowledgement.NEGATIVE
        return Acknowledgement.POSITIVE                 #in case of negative acks 3 retries to be done by server
      