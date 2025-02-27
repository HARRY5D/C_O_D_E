class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def search(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search(root.left, val)
    return search(root.right, val)

root = None
values = [4, 2, 7, 1, 3]
for val in values:
    root = insert(root, val)

result = search(root, 2)
if result: 
    print(result.val, end=' ')
    if result.left:
        print(result.left.val, end=' ')
    if result.right:
        print(result.right.val, end=' ')