import numpy as np

# Part 1: Creating NumPy Arrays
print("\nPart 1: Creating NumPy Arrays\n")

# 1. Using Built-in Methods:
print("\n1- Using Built-in Methods:\n")

# An array of numbers from 0 to 20 with a step of 2.
arr_step2 = np.arange(0, 21, 2)
print("Array from 0 to 20 with a step of 2:", repr(arr_step2))

# A 3x3 identity matrix.
identity_matrix = np.eye(3)
print("\n3x3 Identity matrix:\n", identity_matrix)

# A 4x4 array filled with ones.
ones_array = np.ones((4, 4))
print("\n4x4 array filled with ones:\n", ones_array)

# An array of 10 equally spaced numbers between 5 and 50.
linspace_array = np.linspace(5, 50, 10)
print("\n10 equally spaced numbers between 5 and 50:", repr(linspace_array))


# 2. Creating Arrays from Lists:
print("\n2- Creating Arrays from Lists:\n")

# Convert a Python list [10, 20, 30, 40, 50] into a NumPy array.
list_to_array = np.array([10, 20, 30, 40, 50])
print("\nNumPy array from list:", repr(list_to_array))

# Generate a 3x3 matrix of random numbers using rand(), randn(), and randint().

# rand(): uniform distribution over [0, 1)
rand_matrix = np.random.rand(3, 3)
print("\n3x3 matrix with rand():\n", rand_matrix)

# randn(): standard normal distribution
randn_matrix = np.random.randn(3, 3)
print("\n3x3 matrix with randn():\n", randn_matrix)

# randint(): random integers between low (inclusive) and high (exclusive), e.g. 0 to 10
randint_matrix = np.random.randint(0, 10, (3, 3))
print("\n3x3 matrix with randint():\n", randint_matrix)


# 3. Array Attributes:
print("\n3- Array Attributes:\n")

# Let's pick one array to show its attributes, for example randint_matrix
print("\nAttributes of randint_matrix:")
print("Shape:", randint_matrix.shape)
print("Size:", randint_matrix.size)
print("Data type:", randint_matrix.dtype)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
print("\n#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#\n")

# Part 2: Indexing and Selection
print("\nPart 2: Indexing and Selection\n")

# 1. Basic Indexing and Selection
print("\n1- Basic Indexing and Selection\n")

arr = np.array([5, 10, 15, 20, 25, 30])

print("Original array:", arr)
print("First element:", arr[0])
print("Last three elements:", arr[-3:])
print("Elements at index 1 to 4:", arr[1:5])  # Index 1 to 4 means up to but not including index 5

# 2. Slicing and Views
print("\n2- Slicing and Views\n")

matrix = np.arange(1, 10).reshape(3, 3)
print("\n3x3 matrix:\n", matrix)

print("Second row:", matrix[1])  # row index 1
print("First two columns:\n", matrix[:, :2])
print("Sub-matrix of shape (2,2):\n", matrix[:2, :2])

# 3. Broadcasting
print("\n3- Broadcasting\n")

matrix_broadcast = np.array([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])

# Add 10 to every element
matrix_add10 = matrix_broadcast + 10
print("\nMatrix after adding 10:\n", matrix_add10)

# Multiply the first column by 2
matrix_broadcast[:, 0] = matrix_broadcast[:, 0] * 2
print("Matrix after multiplying first column by 2:\n", matrix_broadcast)

# 4. Copying Arrays
print("\n4- Copying Arrays\n")

# Original array
original = np.array([1, 2, 3, 4, 5])

# Shallow copy (view)
shallow = original.view()
shallow[0] = 99

# Deep copy
deep = original.copy()
deep[1] = 88

print("\nOriginal array after shallow and deep copy modifications:", repr(original))
print("Shallow copy (view):", repr(shallow))
print("Deep copy (independent):", repr(deep))

# 5. Fancy Indexing
print("\n5- Fancy Indexing\n")

arr2 = np.arange(10, 101, 10)
selected_elements = arr2[[0, 3, 5]]
print("\nOriginal array:", repr(arr2))
print("Selected elements at indices [0, 3, 5]:", selected_elements)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
print("\n#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#\n")

# Part 3: NumPy Operations
print("\nPart 3: NumPy Operations\n")

# 1. Mathematical Functions
print("\n1- Mathematical Functions\n")

data = np.array([3, 7, 2, 9, 12, 5, 10])

print("Original array:", repr(data))
print("Maximum value:", np.max(data))
print("Minimum value:", np.min(data))
print("Index of maximum value:", np.argmax(data))
print("Index of minimum value:", np.argmin(data))

# 2. Universal Array Functions
print("\n2- Universal Array Functions\n")

arr = np.array([1, 2, 3, 4, 5])

print("\nOriginal array:", repr(arr))
print("Square root:", repr(np.sqrt(arr)))
print("Exponential:", repr(np.exp(arr)))
print("Sine:", repr(np.sin(arr)))
print("Logarithm:", repr(np.log(arr)))