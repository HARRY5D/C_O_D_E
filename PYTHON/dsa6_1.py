'''
Implement below operations on Binary Tree
(a) Insert a node at Left
(b) Delete a node at Right
(c) Binary Tree Inorder Traversal
(d) Binary Tree Preorder Traversal
(e) Binary Tree Postorder Traversal
(f) Binary Tree Level Order Traversal
Note: for (a) and (b) , First node will be the root node. Display the content of Binary Tree as per Inorder, Preorder, Postorder and Level Order Traversal.

'''
from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert_left(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            current = self.root
            while current.left:
                current = current.left
            current.left = Node(value)

    def delete_right(self):
        if not self.root:
            return
        if not self.root.right:
            self.root = self.root.left
        else:
            parent = self.root
            current = self.root.right
            while current.right:
                parent = current
                current = current.right
            parent.right = current.left

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.value, end=' ')
            self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        if node:
            print(node.value, end=' ')
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.value, end=' ')

    def levelorder_traversal(self, node):
        if node:
            queue = deque([node])
            while queue:
                current_node = queue.popleft()
                print(current_node.value, end=" ")
                if current_node.left:
                    queue.append(current_node.left)
                if current_node.right:
                    queue.append(current_node.right)

def main():
    tree = BinaryTree()
    while True:
        print("\n1. INSERT A NODE AT LEFT")
        print("2. DELETE A NODE AT RIGHT")
        print("3. INORDER TRAVERSAL")
        print("4. PREORDER TRAVERSAL")
        print("5. POSTORDER TRAVERSAL")
        print("6. LEVELORDER TRAVERSAL")
        print("7. Exit")
        choice = input("ENTER YOUR CHOICE : ")

        if choice == '1':
            value = input("ENTER VALUE TO INSERT : ")
            tree.insert_left(value)
        elif choice == '2':
            tree.delete_right()
            print("RIGHTMOST NODE DELETED.")
        elif choice == '3':
            print("Inorder TRAVERSAL: ", end='')
            tree.inorder_traversal(tree.root)
            print()
        elif choice == '4':
            print("Preorder TRAVERSAL: ", end='')
            tree.preorder_traversal(tree.root)
            print()
        elif choice == '5':
            print("Postorder TRAVERSAL: ", end='')
            tree.postorder_traversal(tree.root)
            print()
        elif choice == '6':
            print("LEVEL ORDER TRAVERSAL: ", end='')
            tree.levelorder_traversal(tree.root)
            print()
        elif choice == '7':
            break
        else:
            print("INVALID CHOICE, TRY AGAIN.")

if __name__ == "__main__":
    main()