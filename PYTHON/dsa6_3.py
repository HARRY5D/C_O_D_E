'''
6.3

Custom traversals
(a) Binary Tree Right View
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of 
the nodes which you can see ordered from top to bottom.

(b) (b) Binary Tree boundary
Given a binary tree, print boundary nodes of the binary tree Anti-Clockwise starting from the root.
The boundary includes:
left boundary (nodes on left excluding leaf nodes)
leaves (consist of only the leaf nodes)
right boundary (nodes on right excluding leaf nodes)

Example:
root : 20
left- boundary nodes: 8
leaf nodes: 4 10 14 25
right – boundary nodes: 22


7.1
Perform following operations on BST.
(a)Insert a node in BST
(b)Search a node in BST
You are given the root of a binary search tree (BST) and an integer val.
Find the node in the BST that the node's value equals val and return the subtree rooted with that node.
 If such a node does not exist, return null.
Example 1: Input: root = [4,2,7,1,3], 
val = 2 Output: [2,1,3]

7.2
Kth smallest element in BST
Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
Example 1:
Input: root = [3,1,4,null,2], k = 1
Output: 1
Example 2: Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3

8.1 (a) DFS of Graph You are given a connected undirected graph.
 Perform a Depth First Traversal of the graph. Note: 
 Use a recursive approach to find the DFS traversal of 
 the graph starting from the 0th vertex from left to right
   according to the graph. Example 1:
Input: V = 5 , adj = [[2,3,1] , [0], [0,4], [0], [2]]

Output: 0 2 4 3 1
Explanation:
0 is connected to 2, 3, 1.
1 is connected to 0.
2 is connected to 0 and 4.
3 is connected to 0.
4 is connected to 2.
so starting from 0, it will go to 2 then 4,
and then 3 and 1.
Thus dfs will be 0 2 4 3 1.
(b) BFS of graph Given a directed graph. The task is to do Breadth First Traversal of this graph starting from 0. Note: One can move from node u to node v only if there's an edge from u to v and find the BFS traversal of the graph starting from the 0th vertex, from left to right according to the graph. Also, you should only take nodes directly or indirectly connected from Node 0 in consideration. Example 1:
Input:
Output: 0 1 2 3 4
Explanation:
0 is connected to 1 , 2 , 3.

8.2 Course Schedule (Cycle detection in graph)

There are a total of “numCourses” courses you have to take, labeled from 0 to numCourses - 1. You are given an array named prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1. Return true if you can finish all courses. Otherwise, return false. Example 1: Input: numCourses = 2, prerequisites = [[1,0]] Output: true Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible. Example 2: Input: numCourses = 2, prerequisites = [[1,0],[0,1]] Output: false Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

8.3 Maximum Bomb detonation (Graph edge creation and search) You are given a 
list of bombs. The range of a bomb is defined as the area where its effect can be felt.
This area is in the shape of a circle with the center as the location of the bomb.
The bombs are represented by a 0-indexed 2D integer array “bombs” where
 bombs[i] = [xi, yi, ri]. xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas
ri denotes the radius of its range. You may choose to detonate a single bomb. When a bomb is detonated, it will detonate all
 bombs that lie in its range. These bombs will further detonate the bombs that lie in their ranges. Given the list of bombs, 
 return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb. Example 1:
   Input: bombs = [[2,1,3],[6,1,4]] Output: 2 Explanation:
The above figure shows the positions and ranges of the 2 bombs.

 If we detonate the left bomb, the right bomb will not be affected.
 But if we detonate the right bomb, both bombs will be detonated. So the maximum bombs that can be detonated is max(1, 2) = 2.
 Example 2: Input: bombs = [[1,1,5],[10,10,5]] Output: 1 Explanation: Detonating either bomb will not detonate the other bomb,
so the maximum number of bombs that can be detonated is 1.

Example 3: Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]] Output: 5 Explanation: The best bomb to detonate 
is bomb 0 because: - Bomb 0 detonates bombs 1 and 2. The red circle denotes the range of bomb 0. - Bomb 2 detonates bomb 3.
The blue circle denotes the range of bomb 2. - Bomb 3 detonates bomb 4. The green circle denotes the range of bomb 3.
Thus all 5 bombs are detonated.     

Hashing
1,2
9.1 
Implementing a Hash Table for Student Records Management
Background: You are tasked with implementing a hybrid hash table to manage student records efficiently.
Each student record consists of a unique student ID (key) and the corresponding student score (data). The hash table will support
 two methods of collision handling: separate chaining and linear probing. This flexibility ensures efficient handling of collisions, 
 enabling you to choose the most suitable method based on different scenarios.
Objectives: Hash Table Initialization:
Create a hash table with an appropriate size that is a prime number greater than the initially specified size to reduce collisions. 
Implement a hash function that uses the modulo operation to map keys to indices.
Insertion of Records: Implement functionality to insert student records into the hash table.
Implement both chaining and linear probing for collision handling separately.
Deletion of Records: Implement functionality to delete a record by its key. Ensure the integrity of the hash table after deletion 
for both collision handling methods. Display of Records: Implement functionality to display the contents of the hash table. 
Show all student records stored at each index, clearly indicating which collision handling method is being used.
Requirements: Hash Table Initialization: The hash table should be initialized with a size that is the next prime number 
greater than the specified initial size. The hash function should use the modulo operation to map keys to indices. Insertion:
The insertItem method should allow adding a student ID and score to the hash table. For separate chaining, use linked lists 
to handle collisions. For linear probing, find the next available slot in case of a collision. Deletion: The deleteItem method 
should allow removing a student record based on the student ID. Ensure that the hash table remains functional after a record is deleted.
Display: The displayHash method should output the entire hash table, showing all student records stored at each index.

Clearly distinguish between the records stored using separate chaining and linear probing.
Constraints: Student IDs are integers. Student scores are also integers. The hash table should handle multiple student records having the 
same hash index using linked lists (separate chaining) or linear probing.
Example Usage: Initialize a hash table with an initial size of 6.
Insert the following student records into the hash table using separate chaining:
Student ID: 231, Score: 123 Student ID: 326, Score: 432 Student ID: 212, Score: 523 Student ID: 321, Score: 43 Student ID: 433, Score: 423 
Student ID: 262, Score: 111 Display the hash table.
Delete the record with student ID 212.
Display the hash table again to show the updated records.
Repeat the insertion and deletion steps using linear probing instead of separate chaining, and display the hash table after each operation.
Sample Output: Using Separate Chaining: table[0] --> (231, 123) table[1]

table[2] --> (212, 523) table[3] --> (262, 111) table[4] --> (326, 432) table[5] table[6] --> (321, 43) --> (433, 423)
After deleting record with student ID 212: table[0] --> (231, 123) table[1] table[2] table[3] --> (262, 111) table[4] --> (326, 432) table[5] table[6] --> (321, 43) --> (433, 423)
Using Linear Probing: table[0] --> (231, 123) table[1] --> (321, 43) table[2] table[3] --> (433, 423) table[4] --> (326, 432) table[5] --> (212, 523) table[6] --> (262, 111)
After deleting record with student ID 212: table[0] --> (231, 123) table[1] --> (321, 43) table[2] table[3] --> (433, 423) table[4] --> (326, 432) table[5] table[6] --> (262, 111)

Implementation Notes: Ensure that the hash table size is a prime number for better distribution of keys. Use separate chaining with linked lists and linear probing to handle collisions
 effectively. Implement the insertItem, deleteItem, and displayHash methods to manage and display student records as required.
'''

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rightSideView(root):
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.pop(0)
            if i == level_size - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result

# Example usage
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.right = TreeNode(5)
root.right.right = TreeNode(4)

print(rightSideView(root))  