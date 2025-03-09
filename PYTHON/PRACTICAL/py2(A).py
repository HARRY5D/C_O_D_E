'''
a) Implement following operation using python tuple concept. 
Tuple operation  Create tuples with different data types (integer, float, string, and mixed).
  Access tuple elements using positive and negative indices.  Perform tuple slicing to eitract
   specific portions of the tuple.  Count occurrences of an element and find the indei of an element 
   in a tuple.  Use built-in functions like len(), mai(), min(), and sum() with tuples. 
    Write a program to count and print distinct elements from a tuple.  Convert a list to a tuple 
   and vice versa.  Demonstrate unpacking of tuples into individual variables. b) Implement following 
   operation using Python List concept. List Operation  Create a list of integers, strings, and mixed data 
   types.  Access elements using indices, perform slicing, and update list elements.  Add and remove 
   elements using append(), insert(), remove(), and pop() methods.  Concatenate and repeat lists using 
   operators.  Create a list of squares of the first 10 natural numbers using list comprehension.
      Filter even numbers from a list using list comprehension.  Demonstrate sorting, reversing, and copying lists.
        Write a program to remove duplicates from a list.
         c) Implementing following operation using python dictionaries concept.
         Dictionary Operation:  Create a dictionary to store key-value pairs.  Access, update, and delete dictionary elements using keys.
            Use dictionary methods like keys(), values(), and items().
              Add a new key-value pair and remove an eiisting key-value pair.

'''

print(" TUPLE OPERATIONS ")

t1 = (1, 2, 3, 4, 5)
t2 = (1.1, 2.2, 3.3, 4.4, 5.5)
t3 = ('apple', 'banana', 'orange')
t4 = (1, 2, 2, 3, 2, 4, 5)

mixed = (1, 'hello', 3.14, True)


print(f"Integer tuple: {t1}")
print(f"Float tuple: {t2}")
print(f"String tuple: {t3}")
print(f"mixed tuple: {mixed}")

print(f"First element: {mixed[0]}")
print(f"Last element: {mixed[-1]}")

print(f"First two elements: {mixed[:2]}")
print(f"Last two elements: {mixed[-2:]}")

print(f"Count of 2: {t4.count(2)}")
print(f"Index of first 2: {t4.index(2)}")

print(f"Length: {len(t1)}")
print(f"Maximum: {max(t1)}")
print(f"Minimum: {min(t1)}")
print(f"Sum: {sum(t1)}")


distinct = tuple(set(t4))
print(f"Original tuple: {t4}")
print(f"Distinct tuple: {distinct}")

my_list = [1, 2, 3, 4, 5]
tuple_from_list = tuple(my_list)
list_from_tuple = list(tuple_from_list)
print(f"List to tuple: {tuple_from_list}")
print(f"Tuple to list: {list_from_tuple}")

i, y, z = (1, 2, 3)

print(f"Unpacked values: i={i}, y={y}, z={z}")

print("\n LIST OPERATIONS ")

l1 = [1, 2, 3, 4, 5]
l2 = ['apple', 'banana', 'orange']
l3 = [1, 'hello', 3.14, True]
l4=[1,1,2,3,4,5,5]

print(f"\nInteger list: {l1}")
print(f"String list: {l2}")
print(f"mixed list: {l3}")

l3[1] = 'world'
print(f"Updated list: {l3}")
print(f"Sliced list: {l3[1:3]}")

test_list = [1, 2, 3]
test_list.append(4)
test_list.insert(0, 0)
test_list.remove(2)
topop = test_list.pop()
print(f"Modified list: {test_list}")
print(f"Popped value: {topop}")

list1 = [1, 2]
list2 = [3, 4]
concatenated = list1 + list2
repeated = list1 * 2
print(f"Concatenated: {concatenated}")
print(f"Repeated: {repeated}")

squares = [i**2 for i in range(1, 11)]
print(f"Squares: {squares}")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even = [i for i in numbers if i % 2 == 0]
print(f"Even numbers: {even}")

unsorted = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted = sorted(unsorted)
reverse= list(reversed(unsorted))
print(f"Original: {unsorted}")
print(f"Sorted: {sorted}")
print(f"Reversed: {reverse}")

unique = list(dict.fromkeys(l4))

print(f"Original list: {t4}")
print(f"Without duplicates: {unique}")



# C) DICTIONARY OPERATIONS

student = {
    'name': 'John',
    'age': 20,
    'grade': 'A',
    'courses': ['Math', 'Physics', 'English']
}

print("\n1. Original dictionary:")
print(student)


print("\n2. Access and update:")
print(f"Name: {student['name']}")
student['age'] = 21
print(f"Updated age: {student['age']}")

print("\n3. Dictionary methods:")
print(f"Keys: {list(student.keys())}")
print(f"Values: {list(student.values())}")
print(f"Items: {list(student.items())}")

print("\n4. Add and remove:")
student['email'] = 'john@example.com' 
print("After adding email:", student)

del student['grade'] 
print("After removing grade:", student)

print("\n5. Additional operations:")
print(f"Get grade: {student.get('grade', None)}")

student.update({'grade': 'B', 'semester': 'Fall 2023'})
print("After update:", student)

student_copy = student.copy()
student_copy.clear()
print("Cleared dictionary:", student_copy)



#assignment 

# Create a set

a = set()
print("Initial set:", a)

# Add elements
a.add(10)
a.add(20)
a.add(30)
print("After adding elements:", a)

# Remove an element
a.remove(20)
print("After removing 20:", a)

# Create another set
new_set = {30, 40, 50}
print("Another set:", new_set)

# Combine elements 
combined_set = a.union(new_set)
print("Combined set (union):", combined_set)

# intersection)
common_elements = a.intersection(new_set)
print("Common elements (intersection):", common_elements)

# difference
difference_set = a.difference(new_set)
print("Elements in a but not in new_set:", difference_set)

# symmetric difference
symdiff = a.symmetric_difference(new_set)
print("Symmetric difference:", symdiff)

# subset
sub = a.issubset(combined_set)
print("Is a a subset of combined_set:", sub)
#  superset 
sup = combined_set.issuperset(a)
print("Is combined_set a superset of a:", sup)

# Remove
a.clear()
print("After clearing a:", a)



#assignment 

#5capstone project 1
class EventManagementSystem:
    def __init__(self):
        self.events = {}  # event_name: [(name, contact, department, status), ...]

    def add_participant(self, event_name, name, contact, department):
        if event_name not in self.events:
            self.events[event_name] = []
        participant = (name, contact, department, "Not Attended")
        self.events[event_name].append(participant)
        print(f"Added {name} to {event_name}")

    def display_participants(self, event_name):
        if event_name not in self.events:
            print("Event not found")
            return
        print(f"\nParticipants for {event_name}:")
        for participant in self.events[event_name]:
            print(f"Name: {participant[0]}, Contact: {participant[1]}, "
                  f"Department: {participant[2]}, Status: {participant[3]}")

    def search_participant(self, name):
        found = False
        for event_name, participants in self.events.items():
            for participant in participants:
                if participant[0].lower() == name.lower():
                    print(f"\nFound {name} in {event_name}")
                    print(f"Contact: {participant[1]}")
                    print(f"Department: {participant[2]}")
                    print(f"Status: {participant[3]}")
                    found = True
        if not found:
            print("Participant not found")

    def mark_attendance(self, event_name, name, status):
        if event_name not in self.events:
            print("Event not found")
            return
        
        for i, participant in enumerate(self.events[event_name]):
            if participant[0].lower() == name.lower():
                self.events[event_name][i] = (participant[0], participant[1], 
                                            participant[2], status)
                print(f"Updated {name}'s status to {status}")
                return
        print("Participant not found in this event")

    def generate_summary(self):
        print("\nEvent Summary:")
        for event_name, participants in self.events.items():
            total = len(participants)
            attended = sum(1 for p in participants if p[3] == "Attended")
            print(f"{event_name}: Total: {total}, Attended: {attended}")

# Testing the Event Management System
if __name__ == "__main__":
    ems = EventManagementSystem()

    # Add participants to events
    ems.add_participant("Tech Talk", "John Doe", "1234567890", "Computer Science")
    ems.add_participant("Tech Talk", "Jane Smith", "9876543210", "Electronics")
    ems.add_participant("Cultural Fest", "Alice Johnson", "5555555555", "Arts")

    # Display participants for an event
    ems.display_participants("Tech Talk")

    # Search for a participant
    ems.search_participant("Jane Smith")

    # Mark attendance
    ems.mark_attendance("Tech Talk", "John Doe", "Attended")
    ems.mark_attendance("Tech Talk", "Jane Smith", "Not Attended")

    # Generate summary
    ems.generate_summary()


    #6 capstone project 2

#6. Capstone Project 2: Online Food Delivery System:

#```python
class FoodDeliverySystem:
    def __init__(self):
        self.menu = {
            "Burger": (10.99, "Fast Food"),
            "Pizza": (15.99, "Italian"),
            "Salad": (8.99, "Healthy"),
            "Pasta": (12.99, "Italian"),
            "Ice Cream": (5.99, "Dessert")
        }
        self.orders = []  # [(order_id, customer_name, items, total_bill), ...]
        self.customers = set()
        self.order_counter = 1000

    def display_menu(self):
        print("\nMenu:")
        for item, details in self.menu.items():
            print(f"{item}: ${details[0]} - {details[1]}")

    def place_order(self, customer_name, items):
        if not items:
            print("No items selected")
            return

        total_bill = 0
        valid_items = []
        
        for item in items:
            if item in self.menu:
                valid_items.append(item)
                total_bill += self.menu[item][0]
            else:
                print(f"Item not found: {item}")

        if valid_items:
            order_id = self.order_counter
            self.order_counter += 1
            self.orders.append((order_id, customer_name, valid_items, total_bill))
            self.customers.add(customer_name)
            print(f"\nOrder placed successfully!")
            print(f"Order ID: {order_id}")
            print(f"Items: {', '.join(valid_items)}")
            print(f"Total Bill: ${total_bill:.2f}")
        else:
            print("No valid items in order")

    def calculate_total_revenue(self):
        total_revenue = sum(order[3] for order in self.orders)
        return total_revenue

    def display_unique_customers(self):
        print("\nUnique Customers:")
        for customer in sorted(self.customers):
            print(customer)

# Testing the Food Delivery System
if __name__ == "__main__":
    fds = FoodDeliverySystem()

    # Display menu
    fds.display_menu()

    # Place orders
    fds.place_order("John Doe", ["Burger", "Pizza", "Ice Cream"])
    fds.place_order("Jane Smith", ["Salad", "Pasta"])
    fds.place_order("John Doe", ["Pizza", "Ice Cream"])

    # Calculate and display total revenue
    total_revenue = fds.calculate_total_revenue()
    print(f"\nTotal Revenue: ${total_revenue:.2f}")

    # Display unique customers
    fds.display_unique_customers()
