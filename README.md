# InMemoryQueue


Please run testapplication.py.

python testapplication.py
It will start producers, consumers, inmemory queue.

All requirements implemented 

Requirements:
1. There should be a queue that can receive the message from the producer, and send the
message to the consumer.
2. The queue should be bounded in size and completely held in-memory. Size should be
configurable.
3. The queue should only hold JSON messages.
4. The queue will have at least one producer and multiple consumers.
5. Consumers register callbacks that will be invoked whenever there is a new message
6. Allow subscription of consumers to messages that match a particular expression
7. Consumers might have dependency relationships between them.
For ex :
if there are three consumers A, B and C. One dependency relationship can be that C
cannot consume a particular message before A and B have consumed it.
C -> (A,B) (-> means must process after).
8. Handle concurrent writes and reads consistently between producer and consumers.
9. Provide retry mechanisms to handle failures in message processing. It could be a failure
in publishing or consumption.
10. Handle the message TTL, means the message could expire after some time T. If a
message is expired, it should not be delivered to the consumer.
11. Implementation of sideline (Dead-Letter) queue: move to sideline after retries exhausted.
