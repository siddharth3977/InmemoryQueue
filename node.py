# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:23:48 2022

@author: siddharth
"""

import json
import time
# Node class 
class Node:
   
# Function to initialise the node object
    def __init__(self, message, ttl):
        self.checkMessageFormatJson(message)
        self.data = message # Assign data
        self.next = None # Initialize next as null
        self.prev = None # Initialize prev as null
        self.ttl = self.calculateMessageEndTime(ttl)
        
    def checkMessageFormatJson(self, message):
        try:
            json.loads(message) 
        except Exception as e:
            raise Exception(e)
            
    def calculateMessageEndTime(self,ttl):
        if ttl == 0:
            return 0
        return round(time.time()*1000) + ttl