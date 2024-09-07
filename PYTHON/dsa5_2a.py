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
        self.front = self.rear = 0
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
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.size
        return x

    def print_queue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        print("QUEUE: ", end="")
        for i in range(self.size):
            if self.queue[i] is not None:
                print(self.queue[i], end=" ")
        print()

# Example usage
Q = 5
queries = [[1, 2],[1, 3],[2],[1, 4],[2]]
print("ELEMENTS IN QUEUE : ",queries)
#print(queries)
q = Queue(Q)
for query in queries:
    if query[0] == 1:
        q.enqueue(query[1])
    elif query[0] == 2:
        x = q.dequeue()
        if x is not None:
            print("\nDEQUEUED ELEMENT: ", x,end=' ')
           # print(x, end=' ')

           '''

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, x):
        node = Node(x)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        x = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return x

    def print_queue(self):
        if self.is_empty():
            print("QUEUE IS EMPTY.")
            return
        temp = self.front
        print("QUEUE: ", end="")
        while temp:
            print(temp.data, end=" ")
            temp = temp.next
        print()

# Example usage
Q = 5
queries = [[1, 2],[1, 3],[2],[1, 4],[2]]

print("ELEMENTS IN QUEUE : ",queries)
q = Queue()
for query in queries:
    if query[0] == 1:
        q.enqueue(query[1])
    elif query[0] == 2:
        x = q.dequeue()
        if x is not None:
            print("\nDEQUEUED ELEMENT: ", x,end=' ')