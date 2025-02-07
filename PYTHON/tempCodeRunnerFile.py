
# C) DICTIONARY OPERATIONS
print("\n=== DICTIONARY OPERATIONS ===")

# Create dictionary
student = {
    'name': 'John',
    'age': 20,
    'grade': 'A',
    'courses': ['Math', 'Physics', 'English']
}

print("\n1. Original dictionary:")
print(student)

# Access and update
print("\n2. Access and update:")
print(f"Name: {student['name']}")
student['age'] = 21
print(f"Updated age: {student['age']}")

# Dictionary methods
print("\n3. Dictionary methods:")
print(f"Keys: {list(student.keys())}")
print(f"Values: {list(student.values())}")
print(f"Items: {list(student.items())}")

# Add and remove
print("\n4. Add and remove:")
student['email'] = 'john@example.com'  # Add new key-value pair
print("After adding email:", student)
del student['grade']  # Remove key-value pair
print("After removing grade:", student)

# Additional dictionary operations
print("\n5. Additional operations:")
# Get with default value
print(f"Get grade (default None): {student.get('grade', None)}")

# Update multiple key-value pairs
student.update({'grade': 'B', 'semester': 'Fall 2023'})
print("After update:", student)

# Clear dictionary
student_copy = student.copy()
student_copy.clear()
print("Cleared dictionary:", student_copy)
