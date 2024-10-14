class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def leftBoundary(root, boundary):
    if not root or (not root.left and not root.right):
        return
    boundary.append(root.val)
    if root.left:
        leftBoundary(root.left, boundary)
    elif root.right:
        leftBoundary(root.right, boundary)

def rightBoundary(root, boundary):
    if not root or (not root.left and not root.right):
        return
    if root.right:
        rightBoundary(root.right, boundary)
    elif root.left:
        rightBoundary(root.left, boundary)
    boundary.append(root.val)

def leaves(root, boundary):
    if not root:
        return
    if not root.left and not root.right:
        boundary.append(root.val)
        return
    leaves(root.left, boundary)
    leaves(root.right, boundary)

def boundaryTraversal(root):
    if not root:
        return []
    boundary = [root.val]
    leftBoundary(root.left, boundary)
    leaves(root.left, boundary)
    leaves(root.right, boundary)
    rightBoundary(root.right, boundary)
    return boundary

# Example usage
root = Node(20)
root.left = Node(8)
root.left.left = Node(4)
root.left.right = Node(12)
root.left.right.left = Node(10)
root.left.right.right = Node(14)
root.right = Node(22)
root.right.right = Node(25)

print(boundaryTraversal(root)) 