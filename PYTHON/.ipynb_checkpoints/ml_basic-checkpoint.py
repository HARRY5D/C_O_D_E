import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])               # Create a 1D array
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])     # Create a 2D array
zeros = np.zeros((3, 4))                       # Create array of zeros
ones = np.ones((2, 3))                         # Create array of ones
rng = np.arange(0, 10, 2)                      # Create array from range
linspace = np.linspace(0, 1, 5)               # Create evenly spaced points
rand = np.random.rand(3, 3)                    # Random values between 0-1
randn = np.random.randn(3, 3)                  # Random values (normal distribution)

# Array operations
arr + 5                   # Add to each element
arr * 2                   # Multiply each element
np.sqrt(arr)              # Square root of each element
np.exp(arr)               # e^x for each element
np.log(arr)               # Natural log of each element
np.sin(arr)               # Sine of each element

# Array statistics
arr.sum()                 # Sum of elements
arr.mean()                # Mean
arr.std()                 # Standard deviation
arr.min()                 # Minimum value
arr.max()                 # Maximum value
arr.argmin()              # Index of minimum value
arr.argmax()              # Index of maximum value

# Array shape manipulation
arr.reshape(5, 1)         # Reshape to 5x1
arr.T                     # Transpose
np.vstack((arr, arr))     # Stack vertically
np.hstack((arr, arr))     # Stack horizontally

# Array indexing and slicing
arr[2]                    # 3rd element
arr_2d[1, 2]              # Element at row 1, col 2
arr_2d[:, 0]              # First column
arr_2d[0, :]              # First row
arr_2d[0:2, 1:3]          # Submatrix (rows 0-1, cols 1-2)

# Matrix operations
np.dot(arr_2d, arr_2d.T)  # Matrix multiplication
#np.linalg.inv(arr_2d)     # Matrix inverse (if square and invertible)
#np.linalg.det(arr_2d)     # Determinant