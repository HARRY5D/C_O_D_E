
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
print("\n\nInitial sets:")

print("Set1:", set1)
print("Set2:", set2)

set1.add(7)
print("\nAfter adding 7 to set1:", set1)

set1.discard(7)
print("After removing 7 from set1:", set1)

union_set = set1.union(set2)
print("\nUnion of sets:", union_set)

intersection_set = set1.intersection(set2)
print("Intersection of sets:", intersection_set)

difference_set = set1.difference(set2)
print("Difference (set1 - set2):", difference_set)

symmetric_diff = set1.symmetric_difference(set2)
print("Symmetric difference:", symmetric_diff)

set3 = {1, 2}

print(1 in set1)

print("\nIs {1, 2} subset of set1 ?", set3.issubset(set1))

print("Is set1 superset of {1, 2} ?", set1.issuperset(set3))

set3.clear()

print("After clearing set3:", set3)


#assignment 