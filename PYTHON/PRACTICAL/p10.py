"""
Practical 10: NumPy Operations
This program demonstrates various NumPy operations and array manipulations.
"""

import numpy as np

def basic_numpy_operations():
    print("\n===== BASIC NUMPY OPERATIONS =====")
    
    # Create arrays
    print("Creating arrays:")
    arr1 = np.array([1, 2, 3, 4, 5])
    print("np.array([1, 2, 3, 4, 5]):", arr1)
    
    zeros = np.zeros(5)
    print("np.zeros(5):", zeros)
    
    ones = np.ones(5)
    print("np.ones(5):", ones)
    
    # Range of values
    range_arr = np.arange(0, 10, 2)
    print("np.arange(0, 10, 2):", range_arr)
    
    # Evenly spaced values
    linspace_arr = np.linspace(0, 1, 5)
    print("np.linspace(0, 1, 5):", linspace_arr)
    
    # Element access
    print("\nElement access:")
    print("arr1[2]:", arr1[2])
    print("arr1[1:4]:", arr1[1:4])
    print("arr1[::2]:", arr1[::2])  # Every second element

def array_reshaping():
    print("\n===== ARRAY RESHAPING =====")
    
    # Create a range array
    arr = np.arange(12)
    print("Original array:", arr)
    
    # Reshape to 2D
    arr_2d = arr.reshape(3, 4)
    print("\nReshaped to 3x4 array:")
    print(arr_2d)
    
    # Flatten back to 1D
    flattened = arr_2d.flatten()
    print("\nFlattened back to 1D:", flattened)
    
    # Transpose (swap rows and columns)
    transposed = arr_2d.transpose()
    print("\nTransposed array:")
    print(transposed)

def array_concatenation():
    print("\n===== ARRAY CONCATENATION =====")
    
    # Create two arrays
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    
    print("Array 1:", arr1)
    print("Array 2:", arr2)
    
    # Concatenate
    concatenated = np.concatenate((arr1, arr2))
    print("\nConcatenated:", concatenated)
    
    # 2D arrays
    arr3 = np.array([[1, 2], [3, 4]])
    arr4 = np.array([[5, 6], [7, 8]])
    
    print("\nArray 3:")
    print(arr3)
    print("Array 4:")
    print(arr4)
    
    # Vertical stack (row-wise)
    vstack_result = np.vstack((arr3, arr4))
    print("\nVertical stack:")
    print(vstack_result)
    
    # Horizontal stack (column-wise)
    hstack_result = np.hstack((arr3, arr4))
    print("\nHorizontal stack:")
    print(hstack_result)

def array_manipulation():
    print("\n===== ARRAY MANIPULATION =====")
    
    # Create an array
    arr = np.array([1, 2, 3, 4, 5])
    print("Original array:", arr)
    
    # Append value
    appended = np.append(arr, 6)
    print("After append:", appended)
    
    # Insert value
    inserted = np.insert(arr, 2, 10)  # Insert 10 at index 2
    print("After insert:", inserted)
    
    # Delete value
    deleted = np.delete(arr, 2)  # Delete value at index 2
    print("After delete:", deleted)
    
    # Split array
    split_arr = np.split(arr, [2, 4])  # Split at indices 2 and 4
    print("Split into 3 parts:", split_arr)

def array_slicing_2d():
    print("\n===== 2D ARRAY SLICING =====")
    
    # Create a 2D array
    arr_2d = np.array([[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12]])
    