# C) DICTIONARY 
std = { 's1' : {'name': 'John', 'age': 20, 'grade': 'A'} }

print("\n1. Original dictionary:")
print(std)

print("\n2. Access and update:")
print("Name: ",std['s1']['name'])
std['s1']['age'] = 21
print("Updated age: ",std['s1']['age'])

print("\n3. Dictionary methods:")
print("Keys: ",list(std.keys()))
print("Values: ",list(std.values()))
print("Items: ",list(std.items()))

print("\n4. Add and remove:")
std ['s1']  ['email'] = 'john@example.com'

print("After adding email:", std)

del std['s1']['grade'] 

print("After removing grade:", std)

print("\n5. Additional operations:")

print("Grade : ",std.get('grade'))

std1 = {'grade': 'B', 'semester': 'Fall 2023'}

std['s1'].update(std1)

print("After update:", std)

std_copy = std.copy()
std_copy.clear()
print("Cleared dictionary:", std_copy)


#set  
