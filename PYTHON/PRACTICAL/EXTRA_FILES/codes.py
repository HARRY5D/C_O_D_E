'''
pract 2

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Test the implementation
arr = []
n = int(input("ENTER NO OF ELEMENTS TO ENTER : "))
for i in range(n):
    arr.append(int(input("ENTER ELEMENT {}: ".format(i+1))))
print("ORIGINAL ARRAY:", arr)
arr = bubble_sort(arr)
print("BUBBLE SORTED ARRAY:", arr)

def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# Test the implementation
arr = []
n = int(input("ENTER NO OF ELEMENTS TO ENTER : "))
for i in range(n):
    arr.append(int(input("ENTER ELEMENT {}: ".format(i+1))))
print("ORIGINAL ARRAY:", arr)
arr = selection_sort(arr)
print("SELECTION SORTED ARRAY:", arr)

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

# Test the implementation
arr = []
n = int(input("ENTER NO OF ELEMENTS TO ENTER : "))
for i in range(n):
    arr.append(int(input("ENTER ELEMENT {}: ".format(i+1))))
print("ORIGINAL ARRAY:", arr)
arr = insertion_sort(arr)
print("INSERTION SORTED ARRAY:", arr)

def linear_time_sort(arr):
    n = len(arr)
    first = 0
    second = 0
    for i in range(n-1):
        if arr[i] > arr[i+1]:
            first = i
            break
    for i in range(n-1, first, -1):
        if arr[i] < arr[i-1]:
            second = i
            break
    arr[first], arr[second] = arr[second], arr[first]
    return arr

# Test the implementation
arr = []
n = int(input("ENTER NO OF ELEMENTS TO ENTER : "))
for i in range(n):
    arr.append(int(input("ENTER ELEMENT {}: ".format(i+1))))
print("ORIGINAL ARRAY:", arr)
arr = linear_time_sort(arr)
print("LINEAR TIME SORTED ARRAY:", arr)

'''

'''
pract 3

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.display()

    def delete_last(self):
        if self.head is None:
            print("THE LIST IS EMPTY.")
            return
        if self.head.next is None:
            self.head = None
        else:
            temp = self.head
            while temp.next.next is not None:
                temp = temp.next
            temp.next = None
        self.display()

    def delete_nth_from_end(self, n):
        dummy = Node(0)
        dummy.next = self.head
        first = dummy
        second = dummy

        for i in range(n + 1):
            if first is None:
                print("N IS LARGER THAN LIST'S LENGTH.")
                return
            first = first.next

        while first is not None:
            first = first.next
            second = second.next

        second.next = second.next.next
        self.head = dummy.next
        self.display()

    def delete_all(self):
        self.head = None
        self.display()

    def display(self):
        if self.head is None:
            print("NO ELEMENTS PRESENT.")
            return
        temp = self.head
        while temp is not None:
            print(temp.data, end=" ")
            temp = temp.next
        print()

def main():
    l = LinkedList()
    while True:
        print("CHOOSE FROM BELOW : ")
        print("1. INSERT A NODE AT FRONT.")
        print("2. DELETE A NODE FROM LAST.")
        print("3. DELETE n'th NODE FROM END.")
        print("4. DELETE ALL THE NODES.")
        print("5. EXIT.")

        choice = int(input("ENTER YOUR CHOICE : "))

        if choice == 1:
            data = int(input("ENTER DATA TO INSERT AT FRONT : "))
            l.insert_at_front(data)
        elif choice == 2:
            l.delete_last()
        elif choice == 3:
            n = int(input("ENTER N TO DELETE NODE FROM END(N=1,2..) : "))
            l.delete_nth_from_end(n)
        elif choice == 4:
            l.delete_all()
        elif choice == 5:
            break
        else:
            print("INVALID INPUT.")

if __name__ == "__main__":
    main()



    class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def reverse(self):
        prev = None
        current = self.head
        while current is not None:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        self.head = prev

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.val, end=" ")
            current = current.next
        print()

def main():
    linked_list = LinkedList()
    n = int(input("ENTER TOTAL No. OF ELEMENTS : "))

    for i in range(n):
        val = int(input("ENTER ELEMENT No. " + str(i + 1) + " : "))
        linked_list.append(val)

    print("ORIGINAL LINKED LIST : ")
    linked_list.print_list()

    linked_list.reverse()

    print("REVERSED LINKED LIST : ")
    linked_list.print_list()

if __name__ == "__main__":
    main()


    merging arrays

class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

class MERGE:
    def merge(self, list1, list2):
        dummy = ListNode(0)
        current = dummy
        while list1 is not None and list2 is not None:
            if list1.val < list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        if list1 is not None:
            current.next = list1
        else:
            current.next = list2
        return dummy.next

def main():
    mg = MERGE()

    n1 = int(input("ENTER TOTAL No. OF NODES FOR 1st LIST : "))
    list1 = None
    current1 = None
    for i in range(n1):
        val = int(input("ENTER VALUE FOR NODE " + str(i + 1) + " : "))
        if list1 is None:
            list1 = ListNode(val)
            current1 = list1
        else:
            current1.next = ListNode(val)
            current1 = current1.next

    n2 = int(input("ENTER TOTAL No. OF NODES FOR 2nd LIST : "))
    list2 = None
    current2 = None
    for i in range(n2):
        val = int(input("ENTER VALUE FOR NODE " + str(i + 1) + " : "))
        if list2 is None:
            list2 = ListNode(val)
            current2 = list2
        else:
            current2.next = ListNode(val)
            current2 = current2.next

    MERGER = mg.merge(list1, list2)
    print("Merged list:")
    while MERGER is not None:
        print(MERGER.val, end=" ")
        MERGER = MERGER.next
    print()

if __name__ == "__main__":
    main()

    NODE : 

    class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class List:
    def __init__(self):
        self.head = None

    def insert_at_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        print("NODE INSERTED AT FRONT:", data)
        self.display()

    def delete_last(self):
        if self.head is None:
            print("LINKED LIST IS EMPTY. CANNOT DELETE.")
            return
        if self.head.next is None:
            print("NODE DELETED:", self.head.data)
            self.head = None
            self.display()
            return

        current = self.head
        while current.next.next is not None:
            current = current.next

        print("NODE DELETED:", current.next.data)
        current.next = None
        self.display()

    def delete_nth_from_end(self, n):
        if self.head is None:
            print("LINKED LIST IS EMPTY. CANNOT DELETE.")
            return

        if n <= 0:
            print("INVALID NTH VALUE. PLEASE ENTER A POSITIVE NUMBER.")
            return

        fast = self.head
        slow = self.head

        for _ in range(n):
            if fast is None:
                print("NTH NODE DOES NOT EXIST. INVALID NTH VALUE.")
                return
            fast = fast.next

        if fast is None:
            print("NODE DELETED:", slow.data)
            self.head = self.head.next
            self.display()
            return

        while fast.next is not None:
            fast = fast.next
            slow = slow.next

        if slow.next is not None:
            print("NODE DELETED:", slow.next.data)
            slow.next = slow.next.next
        self.display()

    def delete_all(self):
        if self.head is None:
            print("LINKED LIST IS ALREADY EMPTY.")
            return
        while self.head is not None:
            temp = self.head
            self.head = self.head.next
            temp = None
        print("ALL NODES DELETED.")
        self.display()

    def display(self):
        if self.head is None:
            print("LINKED LIST IS EMPTY.")
            return
        current = self.head
        print("LINKED LIST:", end=" ")
        while current is not None:
            print(current.data, end=" ")
            current = current.next
        print()

def main():
    list_ = List()

    while True:
        print("ENTER 1 TO INSERT A NODE AT FRONT.")
        print("ENTER 2 TO DELETE A NODE AT LAST.")
        print("ENTER 3 TO DELETE NTH NODE FROM END OF LIST.")
        print("ENTER 4 TO DELETE ALL NODES.")
        print("ENTER 5 TO EXIT.")
        choice = int(input("ENTER YOUR CHOICE: "))

        if choice == 1:
            data = int(input("ENTER DATA FOR NEW NODE: "))
            list_.insert_at_front(data)
        elif choice == 2:
            list_.delete_last()
        elif choice == 3:
            n = int(input("ENTER NTH VALUE: "))
            list_.delete_nth_from_end(n)
        elif choice == 4:
            list_.delete_all()
        elif choice == 5:
            print("EXITING.")
            break
        else:
            print("INVALID CHOICE. PLEASE ENTER A NUMBER BETWEEN 1 AND 5.")

if __name__ == "__main__":
    main()


    SORT SWAPPED ELEMENTS : 

    def sort_swapped_elements(arr):
    n = len(arr)
    first = -1
    second = -1

    # Find the two swapped elements
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            if first == -1:
                first = i
            else:
                second = i + 1

    # Swap the two elements
    if second != -1:
        arr[first], arr[second] = arr[second], arr[first]

def main():
    size = int(input("Enter the size of the array: "))
    arr = []
    print("Enter the elements of the array:")
    for i in range(size):
        arr.append(int(input()))

    sort_swapped_elements(arr)

    print("Sorted array: ")
    for i in range(size):
        print(arr[i], end=" ")

if __name__ == "__main__":
    main()

  PRACT -- 3.3

    class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

class MERGE:
    def merge(self, list1, list2):
        dummy = ListNode(0)
        current = dummy
        while list1 is not None and list2 is not None:
            if list1.val < list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        if list1 is not None:
            current.next = list1
        else:
            current.next = list2
        return dummy.next

def main():
    mg = MERGE()

    n1 = int(input("ENTER TOTAL No. OF NODES FOR 1st LIST : "))
    list1 = None
    current1 = None
    for i in range(n1):
        val = int(input("ENTER VALUE FOR NODE " + str(i + 1) + " : "))
        if list1 is None:
            list1 = ListNode(val)
            current1 = list1
        else:
            current1.next = ListNode(val)
            current1 = current1.next

    n2 = int(input("ENTER TOTAL No. OF NODES FOR 2nd LIST : "))
    list2 = None
    current2 = None
    for i in range(n2):
        val = int(input("ENTER VALUE FOR NODE " + str(i + 1) + " : "))
        if list2 is None:
            list2 = ListNode(val)
            current2 = list2
        else:
            current2.next = ListNode(val)
            current2 = current2.next

    MERGER = mg.merge(list1, list2)
    print("Merged list:")
    while MERGER is not None:
        print(MERGER.val, end=" ")
        MERGER = MERGER.next
    print()

if __name__ == "__main__":
    main()
'''