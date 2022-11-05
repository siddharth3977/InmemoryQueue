
import threading
           

class InMemoryQueue:
   
  
    def __init__(self, queueSize):
        self.head = None
        self.last = None
        self.count = 0
        self.capacity = queueSize
        self.lock = threading.Lock()
           
   

    def enqueue(self, node):
        
        self.lock.acquire()
        
        if self.size() == self.capacity:
            self.lock.release()
            raise Exception("queue has already reached its max capacity")
        #print("lock acquired")
        if self.last is None:
            #print("insdied")
            self.head = node
            self.last = self.head
        else:
            self.last.next = node
            self.last.next.prev=self.last
            self.last = self.last.next
        self.count = self.count + 1
        #print("producer going to release lock")
        self.lock.release()
        #print("producer lock released")
               
               

    def dequeue(self):
        #print("consuer going to acquire lock")
        #print(self.size())
        self.lock.acquire()
        #print("lock acquired")
        if self.head is None:
            #print("consumer going to release lock")
            self.lock.release()
            return None
        else:
            msg= self.head.data
            ttl = self.head.ttl
            if self.count == 1:
                self.head = None
                self.last = None
            else:
                self.head = self.head.next
                self.head.prev=None
            self.count = self.count - 1
            #print("consumer going to release lock")
            self.lock.release()
            return msg,ttl
   
   

    def first(self):
        return self.head.data
   
   

    def size(self):
        return self.count
       
       
    
    def isEmpty(self):
   
        if self.head is None:
            return True
        else:
            return False
               
   
    def printqueue(self):
        self.lock.acquire()
        print("queue elements are:")
        temp=self.head
        while temp is not None:
            print(temp.data,end="->")
            temp=temp.next
        self.lock.release()
       