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
       # if node:
            self.inorder_traversal(node.right)
            print(node.value, end=' ')
            self.inorder_traversal(node.left)

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

def main():
    tree = BinaryTree()
    while True:
        print("\n1. Insert a node at Left")
        print("2. Delete a node at Right")
        print("3. Inorder Traversal")
        print("4. Preorder Traversal")
        print("5. Postorder Traversal")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            value = input("Enter the value to insert: ")
            tree.insert_left(value)
        elif choice == '2':
            tree.delete_right()
            print("Rightmost node deleted.")
        elif choice == '3':
            print("Inorder Traversal:")
            tree.inorder_traversal(tree.root)
        elif choice == '4':
            print("Preorder Traversal:")
            tree.preorder_traversal(tree.root)
        elif choice == '5':
            print("Postorder Traversal:")
            tree.postorder_traversal(tree.root)
        
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
