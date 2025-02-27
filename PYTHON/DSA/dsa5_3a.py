'''
(a) Valid Parentheses
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
Example 1:
Input: s = "()"
Output: true"
'''

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

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in bracket_map.values():   
                stack.append(char)
            elif char in bracket_map.keys():  
                if not stack or stack.pop() != bracket_map[char]:
                    return False
        
        return len(stack) == 0 
    
s = input("ENTER EXPRESSION IN BRACKETS : ")

sol = Solution()
result = sol.isValid(s)

print("OUTPUT :",result)

'''
stack = Stack(s)
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)

'''
