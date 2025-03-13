integers = (1, 2, 3, 4, 5, 6, 7, 8, 9)
floats = (1.1, 2.2, 3.3, 4.4, 5.5)
strings = ("a", "b", "c", "d", "e", "f",)
mixed = ("a", 1, "b", 2.2, "c", 3)
print("Positive index ", integers[1])  
print("Negative index ", integers[-1])
print("Tuple slicing:", integers[1:4])
print("Count of 2 in integer:", integers.count(2))  
print("Index of 'b' in string:", strings.index("b"))
print("Length of integer:", len(integers))  
print("Max of integer:", max(integers))  
print("Min of integer:", min(integers))  
print("Sum of integer:", sum(integers))
def count_distinct(tup):
    distinct = set(tup)
    print("Distinct elements:", distinct)
    print("Count of distinct elements:", len(distinct))
count_distinct(mixed)
sample = [1, 2, 3, 4, 5]
converted = tuple(sample)
print("Converted tuple:", converted)  
converted_list = list(converted)
print("Converted list:", converted_list) 


integers = (1, 2, 3, 4, 5, 6, 7, 8, 9)
floats = (1.1, 2.2, 3.3, 4.4, 5.5)
strings = ("a", "b", "c", "d", "e", "f",)
mixed = ("a", 1, "b", 2.2, "c", 3)
print("Positive index ", integers[1])  
print("Negative index ", integers[-1])
print("Tuple slicing:", integers[1:4])
print("Count of 2 in integer:", integers.count(2))  
print("Index of 'b' in string:", strings.index("b"))
print("Length of integer:", len(integers))  
print("Max of integer:", max(integers))  
print("Min of integer:", min(integers))  
print("Sum of integer:", sum(integers))
def count_distinct(tup):
    distinct = set(tup)
    print("Distinct elements:", distinct)
    print("Count of distinct elements:", len(distinct))
count_distinct(mixed)
sample = [1, 2, 3, 4, 5]
converted = tuple(sample)
print("Converted tuple:", converted)  
converted_list = list(converted)
print("Converted list:", converted_list) 


dic = {"name": "H", "age": 20, "city": "Ahmedabad"}
print("Create a dictionary to store key-value pairs:", dic)
name = dic["name"]
print("Access dictionary elements using keys:", dic["name"])
age = dic["age"]
print("Access dictionary elements using keys:", dic["age"])
dic["age"] = 21
print("update dictionary elements using keys:", dic["age"])
del dic["city"]
print("delete dictionary elements using keys:", dic)
keys = dic.keys()
values = dic.values()
items = dic.items()
print("Use dictionary methods like keys()", keys)
print("Use dictionary methods like values()", values)
print("Use dictionary methods like items()", items)
dic["country"] = "India"
print("Add a new key-value pair.", dic["country"])
dic.pop("name")
print("remove an existing key-value pair.", dic)
students = {
    "student1": {"name": "Harnish", "age": 19, "marks": 90},
    "student2": {"name": "Jay", "age": 18, "marks": 85},
}
print("Nested dictionary:", students)
student1_name = students["student1"]["name"]
student2_marks = students["student2"]["marks"]
print("Access nested dictionary elements:", student1_name, student2_marks)
students["student1"]["marks"] = 88
print("Update nested dictionary elements:", students["student1"]["marks"])
dict1 = {"a": 1, "b": 2}
print("dictionary 1:", dict1)
dict2 = {"b": 3, "c": 4}
print("dictionary 2:", dict2)
dict1.update(dict2)
print("Merge two dictionaries using update():", dict2)
unsorted_dict = {"apple": 3, "banana": 1, "cherry": 2}
print("Unsorted dictionary:", unsorted_dict)
sorted_dict = dict(sorted(unsorted_dict.items()))
print("sorted dict:", sorted_dict)


elements = set()
elements.add(1)
elements.add(2)
elements.add(3)
print("Create and Add elements to a set to store unique elements:", elements)
elements.remove(1)
print("Remove elements from a set:", elements)
set1 = {1, 2, 3}
set2 = {3, 4, 5}
combined_set = set1.union(set2)
print("Combine elements from two sets:", combined_set)
common_elements = set1.intersection(set2)
print("Find common elements in two sets:", common_elements)
difference_set = set1.difference(set2)
print("Find difference between two sets:", difference_set)
symmetric_difference_set = set1.symmetric_difference(set2)
print("Find elements present in either of the sets but not in their intersection:",symmetric_difference_set)
s_subset = set1.issubset(set2)
print("Check if set1 is subset of set2:", s_subset)
s_superset = set1.issuperset(set2)
print("Check if set1 is superset of set2:", s_superset)
elements.clear()
print("Clear all elements from a set:", elements)
