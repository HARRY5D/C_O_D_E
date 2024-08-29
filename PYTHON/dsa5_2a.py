'''
Implement Queue using array
Implement a Queue using an Array. Queries in the Queue are of the following type:
(i) 1 x (a query of this type means pushing 'x' into the queue) 
(ii) 2 (a query of this type means to pop element from
 queue and print the popped element) Example 1:
Input:
Q = 5
Queries =
1 2
1 3
2
1 4
2
Output: 2 3
'''
'''
class Queue:
    def __init__(self, size):
        self.queue = [None] * size
        self.front = 0
        self.rear =  0
        self.size = size

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def enqueue(self, x):
        if self.is_full():
            print("QUEUE IS FULL.")
            return
        self.queue[self.rear] = x
        self.rear = (self.rear + 1) % self.size

    def dequeue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        x = self.queue[self.front]
        self.front = (self.front + 1) % self.size
        print("NODE REMOVED : ",x)

    def print_queue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        print("QUEUE: ")
        for i in range(self.size):
            if self.queue[i] is not None:
                print(self.queue[i], end=" ")
        print()
# Example usage
s=int(input("ENTER NO. OF ELEMENTS TO ENTER : "))
q = Queue(s)
queries = [ [0],[2], [3],[ 4], [5] ]
x=int(input("ENTER 1 FOR PUSH,2 FOR POP : "))
if x==1:
        for i in range (1,6):
             y=int(input("ENTER THE VALUE TO BE PUSHED : "))
             q.enqueue(y)
q.print_queue()      
       # y=input(queries[0])
        #q.enqueue(y)
if x == 2:
     print(q.dequeue())
     q.print_queue()

'''
class Queue:
    def __init__(self, size):
        self.queue = [None] * size
        self.front = 0
        self.rear = 0
        self.size = size

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def enqueue(self, x):
        if self.is_full():
            print("QUEUE IS FULL.")
            return
        self.queue[self.rear] = x
        self.rear = (self.rear + 1) % self.size

    def dequeue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        x = self.queue[self.front]
        self.front = (self.front + 1) % self.size
        print("ELEMENTS REMOVED : ", x)
        self.print_queue()

    def print_queue(self):
        print("QUEUE : ", end="")
        for i in range(self.front, self.rear):
            print(self.queue[i % self.size], end=" ")
        print()

# Example usage
q = Queue(5)
queries = [[1, 2],[1, 3],[2],[1, 4],[2]]

print("ELEMENTS IN QUEUE : ",queries)

for query in queries:
    if query[0] == 1:
        q.enqueue(query[1])
        q.print_queue()
    elif query[0] == 2:
        q.dequeue()