#A STACK BY ARRAYS

class Stack:
    def __init__(self, size):
        self.max_size = size
        self.top = -1
        self.stack_array = [None] * size

    def push(self, value):
        if self.top >= self.max_size - 1:
            print("STACK IS FULL", value)
            return
        self.stack_array[self.top + 1] = value
        self.top += 1

    def pop(self):
        if self.top < 0:
            print("STACK IS EMPTY,CAN'T POP.")
            return -1
        value = self.stack_array[self.top]
        self.stack_array[self.top] = None
        self.top =- 1
        return value

stack = Stack(4)
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)

print("ELEMENTS IN STACK(BEFORE POP OPERATION) : ",stack.stack_array)
#print(stack.stack_array)

stack.pop()
print("ELEMENTS IN STACK(AFTER POP OPERATION)  : ",stack.stack_array)
#print(stack.stack_array)



#B  STACK BY LINKED LIST :
 
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top is None:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node

    def pop(self):
        if self.top is None:
            print("STACK IS EMPTY,CAN'T POP.")
            return -1
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data
    def print_stack(self):
        temp = self.top
        while temp:
            print(temp.data, end=" ")
            temp = temp.next
        print()

s = Stack()

s.push(2)
s.push(3)
s.push(4)
print("ELEMENTS IN STACK: ", end="")
s.print_stack()
print("REMOVED ELEMENT : ", s.pop()) 
print("ELEMENTS IN STACK: ", end="")
s.print_stack()