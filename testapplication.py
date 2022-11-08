# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:47:27 2022

@author: siddharth
"""

from inmemoryqueueprocesser import InMemoryQueueProcessor
from inmemoryqueue import InMemoryQueue

from producerthread import ProducerThread
from consumerthead import ConsumerThread

ttl = 1000 #milli secod
message1 = '{"messageId": "def", "httpCode": "200"}'
message2 = '{"messageId": "abc", "httpCode": "400"}'
message3 = '{"messageId": "pt1", "httpCode": "200"}'
message4 = '{"messageId": "pt2", "httpCode": "200"}'

inMemoryQueue = InMemoryQueue(3)  #queus size
inMemoryQueueProcessor = InMemoryQueueProcessor(inMemoryQueue,2)

consumerA = ConsumerThread(1)
consumerB = ConsumerThread(2)
consumerC = ConsumerThread(3)
consumerD = ConsumerThread(4)

inMemoryQueueProcessor.registerConsumer(consumerA, 1,  r'200', [])
inMemoryQueueProcessor.registerConsumer(consumerB, 2,  r'400', [])
inMemoryQueueProcessor.registerConsumer(consumerC, 3, None, [])
inMemoryQueueProcessor.registerConsumer(consumerD, 4, None, [3])

consumerA.start()
consumerB.start()
consumerC.start()
consumerD.start()


messageList = []
messageList.append((message1,ttl))
messageList.append((message2,ttl))
messageList.append((message3,ttl))
messageList.append((message4,ttl))

prosucer = ProducerThread(0, inMemoryQueueProcessor,messageList)
prosucer.start()

prosucer.join()
consumerA.join()
consumerB.join()
consumerC.join()
consumerD.join()

inMemoryQueueProcessor.completeAllTask()
#print(inMemoryQueueProcessor.deadLetterQueue.count)

