# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:48:19 2022

@author: siddharth
"""

class CycleDetector(object):

    def checkCyclicDependency(self, subscriptionMap1):
        subscriptionMap = dict(subscriptionMap1)
        visited = set()
        
        def dfs(customerid):
            
            if customerid in visited:
                return False
            
            if customerid not in subscriptionMap or len(subscriptionMap[customerid])==0:
                return True
            
            visited.add(customerid)
            for c in subscriptionMap[customerid]:
                ans = dfs(c)
                if not ans:
                    return False
            subscriptionMap[customerid] = []
            visited.remove(customerid)
            return True
        

        for customerid in subscriptionMap:
            if not dfs(customerid):
                return False
        return True