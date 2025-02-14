
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


# from collections import Counter

# #Tuple Operations

# my_tuple = (1, 2, 2, 3, 4, 4, 5)
# unique = tuple(sorted(set(my_tuple)))

# print("Original tuple:", my_tuple)
# print("Tuple with duplicates removed:", unique)

# students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]

# sorted_students = sorted(students, key=lambda x: x[1], reverse=True)

# print("\nList of students sorted by marks:", sorted_students)


# my_tuple = (1, 2, 2, 3, 4, 4, 5, 2)
# freq = Counter(my_tuple)
# print("\nFrequency of elements in the tuple:", freq)

# # Implement a tuple-based record system where each tuple represents a record (ID, Name, and Marks) and perform search operations.
# records = [(1, "Alice", 85), (2, "Bob", 92), (3, "Charlie", 78)]

# def search_record(record_id):
#     for record in records:
#         if record[0] == record_id:
#             return record
#     return None

# search_id = 2
# found_record = search_record(search_id)
# if found_record:
#     print(f"\nRecord found for ID {search_id}:", found_record)
# else:
#     print(f"\nNo record found for ID {search_id}")
    

#list operation
'''
print("\n8. List Operations:")

# Implement a program to generate a list of prime numbers within a given range.
def generate_primes(start, end):
    primes = []
    for num in range(start, end + 1):
        if num > 1:
            for i in range(2, int(num**0.5) + 1):
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
    return primes

start_range = 1
end_range = 50
prime_numbers = generate_primes(start_range, end_range)
print("Prime numbers between", start_range, "and", end_range, ":", prime_numbers)

# Flatten a nested list using recursion.
def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

nested_list = [1, [2, [3, 4], 5], 6]
flat_list = flatten_list(nested_list)
print("\nFlattened list:", flat_list)

# Write a program to find the second largest element from a list without using built-in functions.
def find_second_largest(input_list):
    if len(input_list) < 2:
        return "List must contain at least two elements"
    
    largest = second_largest = float('-inf')
    
    for num in input_list:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    
    if second_largest == float('-inf'):
        return "No second largest element found"
    
    return second_largest

my_list = [10, 5, 8, 20, 15]
second_largest = find_second_largest(my_list)
print("\nSecond largest element:", second_largest)

# Use a list to manage a task queue, where tasks are added, removed, and processed sequentially.
task_queue = []

def add_task(task):
    task_queue.append(task)
    print("Task added:", task)

def process_task():
    if task_queue:
        task = task_queue.pop(0)
        print("Processing task:", task)
    else:
        print("No tasks in the queue")

add_task("Task 1")
add_task("Task 2")
process_task()
process_task()
process_task()
'''
#dictionary oper.n

'''
print("\n9. Dictionary Operations:")

# Write a program to count the frequency of each word in a string and store it in a dictionary.
def word_frequency(input_string):
    words = input_string.lower().split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

my_string = "This is a test string. This string is a test."
word_freq = word_frequency(my_string)
print("Word frequency:", word_freq)

# Implement a simple phonebook application using a dictionary where users can add, delete, and search for contacts.
phonebook = {}

def add_contact(name, phone):
    phonebook[name] = phone
    print(f"Added {name} with phone number {phone}")

def delete_contact(name):
    if name in phonebook:
        del phonebook[name]
        print(f"Deleted {name} from phonebook")
    else:
        print(f"{name} not found in phonebook")

def search_contact(name):
    if name in phonebook:
        print(f"Phone number for {name}: {phonebook[name]}")
    else:
        print(f"{name} not found in phonebook")

add_contact("Alice", "123-456-7890")
add_contact("Bob", "987-654-3210")
search_contact("Alice")
delete_contact("Bob")
search_contact("Bob")

# Create a dictionary of students and their grades. Write a program to filter students who scored more than a specific mark.
students = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 95}

def filter_students(grade_threshold):
    filtered_students = {name: grade for name, grade in students.items() if grade > grade_threshold}
    return filtered_students

threshold = 80
top_students = filter_students(threshold)
print(f"\nStudents who scored more than {threshold}:", top_students)

# Write a program to convert a list of tuples (key-value pairs) into a dictionary and vice versa.
list_of_tuples = [("a", 1), ("b", 2), ("c", 3)]

def list_to_dict(list_of_tuples):
    return dict(list_of_tuples)

def dict_to_list(my_dict):
    return list(my_dict.items())

my_dictionary = list_to_dict(list_of_tuples)
print("\nList of tuples converted to dictionary:", my_dictionary)

my_list = dict_to_list(my_dictionary)
print("Dictionary converted back to list of tuples:", my_list)
'''