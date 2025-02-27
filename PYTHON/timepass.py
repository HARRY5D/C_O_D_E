
print("\n=== DICTIONARY OPERATIONS ===")

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
student['email'] = 'john@example.com'  # Add new key-value pair
print("After adding email:", student)
del student['grade']  # Remove key-value pair
print("After removing grade:", student)

print("\n5. Additional operations:")

print(f"Get grade (default None): {student.get('grade', None)}")

student.update({'grade': 'B', 'semester': 'Fall 2023'})
print("After update:", student)

student_copy = student.copy()
student_copy.clear()
print("Cleared dictionary:", student_copy)

#all codes 


from collections import Counter
from typing import Tuple, List

# 1. Remove duplicates from tuple
def remove_duplicates(tup: Tuple) -> Tuple:
    return tuple(dict.fromkeys(tup))

# 2. Sort students by marks
def sort_students_by_marks(students: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    return sorted(students, key=lambda x: x[1], reverse=True)

# 3. Count frequency using Counter
def count_frequency(tup: Tuple) -> dict:
    return dict(Counter(tup))

# 4. Tuple-based record system
class StudentRecords:
    def __init__(self):
        self.records = []
    
    def add_record(self, id: int, name: str, marks: int):
        self.records.append((id, name, marks))
    '''
    def search_by_id(self, id: int) -> Tuple:
        return next((record for record in self.records if record[0] == id), None)
    '''
    def search_by_name(self, name: str) -> List[Tuple]:
        return [record for record in self.records if record[1].lower() == name.lower()]

# Testing the implementations
if __name__ == "__main__":
    # Test remove duplicates
    test_tuple = (1, 2, 2, 3, 3, 4, 5, 5)
    print("Original tuple:", test_tuple)
    print("After removing duplicates:", remove_duplicates(test_tuple))

    # Test student sorting
    students = [("John", 85), ("Alice", 92), ("Bob", 78), ("Eve", 95)]
    print("\nSorted students by marks:", sort_students_by_marks(students))

    # Test frequency counting
    freq_tuple = (1, 2, 2, 3, 3, 3, 4, 4, 4, 4)
    print("\nFrequency count:", count_frequency(freq_tuple))

    # Test record system
    records = StudentRecords()
    records.add_record(1, "John", 85)
    records.add_record(2, "Alice", 92)
    records.add_record(3, "Bob", 78)
    '''
    print("\nSearch by ID (1):", records.search_by_id(1))
    print("Search by name (Alice):", records.search_by_name("Alice"))
'''

#2
    from typing import List

# 1. Generate prime numbers
def generate_primes(start: int, end: int) -> List[int]:
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    return [num for num in range(start, end + 1) if is_prime(num)]

# 2. Flatten nested list
def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

''' # 3. Find second largest without built-in functions
def find_second_largest(numbers: List[int]) -> int:
    if len(numbers) < 2:
       return None
    
    largest = second_largest = float('-inf')
    for num in numbers:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num < largest:
            second_largest = num
    
    return second_largest if second_largest != float('-inf') else None
'''
# 4. Task Queue Manager
class TaskQueue:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task: str):
        self.tasks.append(task)
        print(f"Added task: {task}")
    
    def remove_task(self) -> str:
        if self.tasks:
            return self.tasks.pop(0)
        return "No tasks available"
    
    def process_next_task(self):
        task = self.remove_task()
        if task != "No tasks available":
            print(f"Processing task: {task}")
        else:
            print(task)
    
    def view_tasks(self):
        return self.tasks

# Testing the implementations
if __name__ == "__main__":
    # Test prime numbers
    print("Prime numbers between 1 and 20:", generate_primes(1, 20))

    # Test flatten list
    nested = [1, [2, 3, [4, 5]], 6, [7, 8]]
    print("\nFlattened list:", flatten_list(nested))

    # Test second largest
    numbers = [10, 5, 8, 12, 3, 7, 9]
    #print("\nSecond largest number:", find_second_largest(numbers))

    # Test task queue
    queue = TaskQueue()
    print("\nTask Queue Operations:")
    queue.add_task("Write report")
    queue.add_task("Send email")
    queue.add_task("Schedule meeting")
    print("Current tasks:", queue.view_tasks())
    queue.process_next_task()
    print("Remaining tasks:", queue.view_tasks())


#3
    from typing import Dict, List, Tuple

# 1. Word frequency counter
def count_word_frequency(text: str) -> Dict[str, int]:
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# 2. Phone Book Application
class PhoneBook:
    def __init__(self):
        self.contacts = {}
    
    def add_contact(self, name: str, number: str):
        self.contacts[name] = number
        print(f"Added contact: {name}")
    
    def delete_contact(self, name: str):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Deleted contact: {name}")
        else:
            print("Contact not found")
    
    def search_contact(self, name: str) -> str:
        return self.contacts.get(name, "Contact not found")
    
    def view_contacts(self):
        return self.contacts

# 3. Student Grade Filter
class GradeBook:
    def __init__(self):
        self.grades = {}
    
    def add_student(self, name: str, grade: float):
        self.grades[name] = grade
    
    def filter_by_grade(self, min_grade: float) -> Dict[str, float]:
        return {name: grade for name, grade in self.grades.items() if grade >= min_grade}

# 4. Convert between list of tuples and dictionary
def tuples_to_dict(tuple_list: List[Tuple]) -> Dict:
    return dict(tuple_list)

def dict_to_tuples(dictionary: Dict) -> List[Tuple]:
    return list(dictionary.items())

# Testing the implementations
if __name__ == "__main__":
    # Test word frequency
    text = "the quick brown fox jumps over the lazy dog"
    print("Word frequency:", count_word_frequency(text))

    # Test phone book
    phone_book = PhoneBook()
    print("\nPhone Book Operations:")
    phone_book.add_contact("John", "1234567890")
    phone_book.add_contact("Alice", "9876543210")
    print("All contacts:", phone_book.view_contacts())
    print("Search Alice:", phone_book.search_contact("Alice"))
    phone_book.delete_contact("John")
    print("Updated contacts:", phone_book.view_contacts())

    # Test grade book
    grade_book = GradeBook()
    grade_book.add_student("John", 85)
    grade_book.add_student("Alice", 92)
    grade_book.add_student("Bob", 78)
    print("\nStudents with grades >= 80:", grade_book.filter_by_grade(80))

    # Test tuple-dict conversion
    tuple_list = [("a", 1), ("b", 2), ("c", 3)]
    dictionary = tuples_to_dict(tuple_list)
    print("\nTuples to dict:", dictionary)
    print("Dict to tuples:", dict_to_tuples(dictionary))

#4
    # 1. Remove duplicates using set
def remove_duplicates_using_set(lst):
    return list(set(lst))

# 2. Symmetric difference of multiple sets
def symmetric_difference_multiple_sets(*sets):
    if not sets:
        return set()
    result = sets[0]
    for s in sets[1:]:
        result = result.symmetric_difference(s)
    return result

# 3. Intersection of even and prime numbers
def even_prime_intersection(limit):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    even_numbers = set(range(0, limit + 1, 2))
    prime_numbers = {n for n in range(2, limit + 1) if is_prime(n)}
    return even_numbers.intersection(prime_numbers)

# 4. Union of odd numbers and multiples of 9
def odd_multiples_of_nine_union(limit):
    odd_numbers = {n for n in range(1, limit + 1, 2)}
    multiples_of_nine = {n for n in range(9, limit + 1, 9)}
    return odd_numbers.union(multiples_of_nine)

# 5. Difference of positive and negative numbers
def positive_negative_difference(numbers):
    positive = {n for n in numbers if n > 0}
    negative = {n for n in numbers if n < 0}
    return positive.difference(negative)

# Testing the implementations
if __name__ == "__main__":
    # Test remove duplicates
    duplicate_list = [1, 2, 2, 3, 3, 4, 5, 5]
    print("Original list:", duplicate_list)
    print("After removing duplicates:", remove_duplicates_using_set(duplicate_list))

    # Test symmetric difference
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    set3 = {3, 4, 5}
    print("\nSymmetric difference:", symmetric_difference_multiple_sets(set1, set2, set3))

    # Test even-prime intersection
    print("\nEven prime numbers up to 20:", even_prime_intersection(20))

    # Test odd-multiple of 9 union
    print("\nUnion of odd numbers and multiples of 9 up to 50:", 
          odd_multiples_of_nine_union(50))

    # Test positive-negative difference
    numbers = {-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5}
    print("\nDifference of positive and negative numbers:", 
          positive_negative_difference(numbers))
    
    

    #7

    #8
    #9
    #10
