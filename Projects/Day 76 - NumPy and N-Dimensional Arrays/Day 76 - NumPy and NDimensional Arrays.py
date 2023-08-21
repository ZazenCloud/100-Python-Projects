import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image

# Create a ndarray
my_array = np.array([1.1, 9.2, 8.1, 4.7])

# Show rows and columns
my_array.shape

# Access element by index
my_array[2]

# Show dimensions of an array
my_array.ndim

# Create a 2D array
array_2d = np.array(
    [
        [1, 2, 3, 9],
        [5, 6, 7, 8]
    ]
)

# Creating an array with with the 'arange' function
a = np.arange(10, 30)
print(a)

# Slicing an array
print(a[-3:])
print(a[3:6])
print(a[12:])
print(a[::2])

# Flipping an array
print(np.flip(a))

# Printing out all the indices of the non-zero elements of an array
some_array = np.array([6, 0, 9, 0, 0, 5, 0])
non_zero_indices = np.nonzero(some_array)
print(non_zero_indices)

# Generating a random 3x3x3 array
random_array = np.random.random((3, 3, 3))
print(random_array)

# Creating a vector with evenly spaced out values
x = np.linspace(0, 100, 9)
print(x)

# Plotting two vectors
y = np.linspace(-3, 3, 9)
plt.plot(x, y)
plt.show()

# Creating a noise image and displaying it
noise = np.random.random((128, 128, 3))
plt.imshow(noise)

# Linear Algebra with vectors
v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])
print(v1 + v2)
print(v1 * v2)

# Broadcasting
array_2d = np.array(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8]
    ]
)
print(array_2d + 10)
print(array_2d * 2)

# Matrix multiplication
a1 = np.array(
    [
        [1, 3],
        [0, 1],
        [6, 2],
        [9, 7]
    ]
)
b1 = np.array(
    [
        [4, 1, 3],
        [5, 8, 5]
    ]
)
c = np.matmul(a1, b1)
print(c)
# or
c = a1 @ b1
print(c)

# Default image (racoon)
img = misc.face()

# Display image
plt.imshow(img)

# Image info (type, shape, dimensions)
type(img)
img.shape
img.ndim

# Converting to B&W
grey_vals = np.array([0.2126, 0.7152, 0.0722])
sRGB_img = img / 255
gray_img = sRGB_img @ grey_vals
plt.imshow(gray_img, cmap='gray')

# Flipping image
plt.imshow(np.flip(gray_img), cmap='gray')

# Rotating image
plt.imshow(np.rot90(img))

# Solarizing image
plt.imshow(255 - img)

# Opening external image
file_name = 'yummy_macarons.jpg'
my_img = Image.open(file_name)

# Transforming image into an array
img_array = np.array(my_img)

# Solarizing image
plt.imshow(255 - img_array)
