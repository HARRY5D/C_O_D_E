'''
Maximum Depth of Binary Tree
Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
Example 1:
Input: root = [3,9,20, null, null,15,7]
Output: 3

'''

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def maxDepth(root):
    if root is None:
        return 0
    else:
        return 1 + max(maxDepth(root.left), maxDepth(root.right))

root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print("ELEMENTS IN BINARY TREE = [3,9,20, null, null,15,7]")

print("OUTPUT : ",maxDepth(root))  