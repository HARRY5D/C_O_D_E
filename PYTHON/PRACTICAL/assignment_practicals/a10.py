# """
# NumPy is a powerful library for numerical computing in Python.
# It provides support for multi-dimensional arrays and matrices,
# along with a collection of mathematical functions to operate on these arrays.
# Array Creation:

# np.array() to create arrays from lists or tuples
# np.zeros() and np.ones() for arrays filled with specific values
# np.arange() and np.linspace() for creating arrays with ranges
# Reshaping and Transformation:

# np.reshape() to change array dimensions
# np.flatten() to convert multi-dimensional arrays to 1D
# np.transpose() to swap rows and columns
# Joining and Splitting:

# np.concatenate() to join arrays
# np.split() to divide arrays
# np.vstack() and np.hstack() for vertical and horizontal stacking
# Array Modification:

# np.append() to add elements
# np.delete() to remove elements
# np.insert() to place elements at specific positions
# Indexing and Slicing:

# Single element access with arr[i]
# Basic slicing with arr[i:j]
# Step slicing with arr[start:end:step]
# Multi-dimensional slicing with arr[:, :]
# """ 

# import numpy as np

# # # Basic Array Creation
# # print("===== ARRAY CREATION =====")

# # Create array from list or tuple
# list_array = np.array([1, 2, 3, 4, 5])
# print("From list:", list_array)

# tuple_array = np.array((6, 7, 8, 9, 10))
# print("From tuple:", tuple_array)

# # Create arrays with specific values
# zeros_array = np.zeros(5)
# print("Zeros array:", zeros_array)

# ones_array = np.ones(5)
# print("Ones array:", ones_array)

# # Create arrays with ranges
# range_array = np.arange(0, 10, 2)  # start, stop, step
# print("Range array:", range_array)

# linspace_array = np.linspace(0, 1, 5)  # start, stop, num_points
# print("Linspace array:", linspace_array)

# # Multi-dimensional arrays
# # print("\n===== MULTI-DIMENSIONAL ARRAYS =====")

# # Create a 2D array (matrix)
# matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print("2D Matrix:")
# print(matrix)

# # Create a 3x3 matrix of zeros
# zeros_matrix = np.zeros((3, 3))
# print("\nZeros matrix:")
# print(zeros_matrix)

# # Create a 2x3 matrix of ones
# ones_matrix = np.ones((2, 3))
# print("\nOnes matrix:")
# print(ones_matrix)

# # Reshape arrays
# # print("\n===== RESHAPING ARRAYS =====")

# # Reshape 1D to 2D
# reshaped_array = np.arange(10).reshape(2, 5)
# print("Reshaped from 1D to 2D:")
# print(reshaped_array)

# # Flatten a 2D array to 1D
# flattened_array = matrix.flatten()
# print("\nFlattened 2D to 1D:", flattened_array)

# # Transpose (swap rows and columns)
# transposed = np.transpose(matrix)
# print("\nTransposed matrix:")
# print(matrix)
# print("becomes:")
# print(transposed)

# # Array Joining and Splitting
# # print("\n===== JOINING AND SPLITTING =====")

# # Concatenate arrays
# array1 = np.array([1, 2, 3])
# array2 = np.array([4, 5, 6])
# concatenated = np.concatenate((array1, array2))
# print("Concatenated:", concatenated)

# # Vertical stacking (row-wise)
# vstacked = np.vstack((array1, array2))
# print("\nVertically stacked:")
# print(vstacked)

# # Horizontal stacking (column-wise)
# hstacked = np.hstack((array1, array2))
# print("\nHorizontally stacked:", hstacked)

# # Split array into multiple sub-arrays
# split_arrays = np.split(concatenated, 3)  # Split into 3 equal parts
# print("\nSplit into 3 parts:", split_arrays)

# # Array Modification
# # print("\n===== ARRAY MODIFICATION =====")

# # Append values
# appended = np.append(array1, [7, 8, 9])
# print("Appended array:", appended)

# # Delete elements
# deleted = np.delete(appended, [1, 3, 5])  # Delete elements at indices 1, 3, 5
# print("After deletion:", deleted)

# # Insert values
# inserted = np.insert(array1, 1, 42)  # Insert 42 at position 1
# print("After insertion:", inserted)

# # Indexing and Slicing
# # print("\n===== INDEXING AND SLICING =====")

# arr = np.arange(10)
# print("Original array:", arr)

# # Access single element
# print("Element at index 3:", arr[3])

# # Slice from index 2 to 7 (exclusive)
# print("Slice [2:7]:", arr[2:7])

# # Slice with step
# print("Slice [1:8:2]:", arr[1:8:2])  # From 1 to 8 with step 2

# # 2D array slicing
# print("\n2D array:")
# print(matrix)

# # Get first row
# print("First row:", matrix[0])

# # Get first column
# print("First column:", matrix[:, 0])

# # Get a submatrix (middle elements)
# print("Middle submatrix:")
# print(matrix[0:2, 0:2])

# # Advanced usage
# # print("\n===== ADVANCED EXAMPLES =====")

# # Create a 3x3x3 cube
# cube = np.arange(27).reshape(3, 3, 3)
# print("3D cube shape:", cube.shape)

# # Access elements in 3D array
# print("First layer of cube:")
# print(cube[0])

# # Element-wise operations
# a = np.array([1, 2, 3])
# b = np.array([4, 5, 6])
# print("\nElement-wise addition:", a + b)
# print("Element-wise multiplication:", a * b)

# # Broadcasting (operations between arrays of different shapes)
# scalar = 5
# print("\nMultiply array by scalar:", a * scalar)

# # Statistical operations
# data = np.array([1, 2, 3, 4, 5])
# print("\nSum:", np.sum(data))
# print("Mean:", np.mean(data))
# print("Max:", np.max(data))
# print("Min:", np.min(data))
# print("Standard deviation:", np.std(data))

# # Boolean indexing
# print("\nElements greater than 3:", data[data > 3])


import numpy as np

list_array = np.array([1, 2, 3, 4, 5])
print("From list:", list_array)

tuple_array = np.array((6, 7, 8, 9, 10))
print("From tuple:", tuple_array)

zeros_array = np.zeros(5)
print("Zeros array:", zeros_array)

ones_array = np.ones(5)
print("Ones array:", ones_array)

range_array = np.arange(0, 10, 2)
print("Range array:", range_array)

linspace_array = np.linspace(0, 1, 5)
print("Linspace array:", linspace_array)

matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("2D Matrix:")
print(matrix)

zeros_matrix = np.zeros((3, 3))
print("\nZeros matrix:")
print(zeros_matrix)

ones_matrix = np.ones((2, 3))
print("\nOnes matrix:")
print(ones_matrix)

reshaped_array = np.arange(10).reshape(2, 5)
print("Reshaped from 1D to 2D:")
print(reshaped_array)

flattened_array = matrix.flatten()
print("\nFlattened 2D to 1D:", flattened_array)

transposed = np.transpose(matrix)
print("\nTransposed matrix:")
print(matrix)
print("becomes:")
print(transposed)

array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])
concatenated = np.concatenate((array1, array2))
print("Concatenated:", concatenated)

vstacked = np.vstack((array1, array2))
print("\nVertically stacked:")
print(vstacked)

hstacked = np.hstack((array1, array2))
print("\nHorizontally stacked:", hstacked)

split_arrays = np.split(concatenated, 3)
print("\nSplit into 3 parts:", split_arrays)

appended = np.append(array1, [7, 8, 9])
print("Appended array:", appended)

deleted = np.delete(appended, [1, 3, 5])
print("After deletion:", deleted)

inserted = np.insert(array1, 1, 42)
print("After insertion:", inserted)

arr = np.arange(10)
print("Original array:", arr)

print("Element at index 3:", arr[3])

print("Slice [2:7]:", arr[2:7])

print("Slice [1:8:2]:", arr[1:8:2])

print("\n2D array:")
print(matrix)

print("First row:", matrix[0])

print("First column:", matrix[:, 0])

print("Middle submatrix:")
print(matrix[0:2, 0:2])

cube = np.arange(27).reshape(3, 3, 3)
print("3D cube shape:", cube.shape)

print("First layer of cube:")
print(cube[0])

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("\nElement-wise addition:", a + b)
print("Element-wise multiplication:", a * b)

scalar = 5
print("\nMultiply array by scalar:", a * scalar)

data = np.array([1, 2, 3, 4, 5])
print("\nSum:", np.sum(data))
print("Mean:", np.mean(data))
print("Max:", np.max(data))
print("Min:", np.min(data))
print("Standard deviation:", np.std(data))

print("\nElements greater than 3:", data[data > 3])

