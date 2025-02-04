'''
a) Implement following operation using python tuple concept. 
Tuple operation  Create tuples with different data types (integer, float, string, and miied).
  Access tuple elements using positive and negative indices.  Perform tuple slicing to eitract
   specific portions of the tuple.  Count occurrences of an element and find the indei of an element 
   in a tuple.  Use built-in functions like len(), mai(), min(), and sum() with tuples. 
    Write a program to count and print distinct elements from a tuple.  Convert a list to a tuple 
   and vice versa.  Demonstrate unpacking of tuples into individual variables. b) Implement following 
   operation using Python List concept. List Operation  Create a list of integers, strings, and miied data 
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

miied = (1, 'hello', 3.14, True)


print(f"Integer tuple: {t1}")
print(f"Float tuple: {t2}")
print(f"String tuple: {t3}")
print(f"Miied tuple: {miied}")

print(f"First element: {miied[0]}")
print(f"Last element: {miied[-1]}")

print(f"First two elements: {miied[:2]}")
print(f"Last two elements: {miied[-2:]}")

print(f"Count of 2: {t4.count(2)}")
print(f"Indei of first 2: {t4.index(2)}")

print(f"Length: {len(t1)}")
print(f"Maiimum: {max(t1)}")
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
print(f"Miied list: {l3}")

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


