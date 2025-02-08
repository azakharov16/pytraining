### Warm-up ###
import warnings

def sqr(x):
    if x < 0:
        warnings.warn("NOTE: you have supplied a negative argument")
    return x ** 2
print(sqr(-2))

# Turn the warnings off locally
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(sqr(-4))

### Basic arithmetics with numpy ###
from math import sqrt, log
from pprint import pprint

print(sqrt(-1))  # error
print(log(0))  # error

import numpy as np

print(np.sqrt(-1))  # warning, returns np.nan object (Not A Number)
print(np.log(0))  # warning, returns np.inf object (infinity)

# Turn the warnings off globally
warnings.filterwarnings("ignore")
print(np.log(0))

# Some properties of np.nan and np.inf
print(1 + np.nan)
print(1 > np.nan)
print(1 < np.nan)
print(np.nan + np.nan)
print(np.nan == np.nan)
print(np.isnan(np.nan))
print(1 + np.inf)
print(np.inf - 1)
print(np.inf + np.inf)
print(np.inf + np.nan)
print(np.inf - np.inf)
print(np.inf > np.nan)

### Numpy built-in common mathematical functions ###
# - np.round(), np.floor(), np.ceil()
# - np.sqrt(), np.log(), np.exp(), np.mod()
# - Math constants: np.pi, np.e
# - np.sin(), np.cos(), np.tan(), np.sinc(), np.sinh(), np.cosh(), np.tanh()
# - np.arcsin(), np.arccos(), np.arctan(), np.arcsinh(), np.arccosh(), np.arctanh()

# NOTE: all functions are vectorized to work with numerical arrays of type np.ndarray

### Manipulating multidimensional numeric arrays ###
# Constructing an ndarray
a = np.array([1,2,3], dtype = float)
print(type(a))
print(a.dtype)
a = a.astype(int)
print(a.dtype)
print(a.tolist())
# NOTE: only data of the same type can be stored in numpy arrays

# Slicing
b = np.array([[1,2,3],[4,5,6]], dtype = float)
print(b.shape)
print(len(b))  #length of first axis
print(b[0, 1])
print(b[1, 0])
print(b[1, 1])
print(b[1, 2])
print(b[0, :])
print(b[1, :])
print(b[-1, :])
print(b[-1, -2:])
print(b[:-1, :-2])
print(b[-1:, :-1])
pprint(b >= 2)
pprint(b[b >= 2])

# NOTE: numpy arrays are mutable, thus subject to name binding

# Shape transformations
pprint(b.transpose())
pprint(b.flatten())
pprint(b.reshape(3,2))

a = np.array([[1,2],[3,4]], int)
b = np.array([[5,6],[7,8]], int)
pprint(np.concatenate((a,b),axis=0))
pprint(np.concatenate((a,b),axis=1))
print(np.append(a,b))  # if axis is None, flattens both arrays
pprint(np.append(a,b,axis=0))  # the same as np.concatenate()
pprint(np.append(a,b,axis=1))  # the same as np.concatenate()
# NOTE that np.concatenate() does not require the arrays to be of the same shape
# in the dimension corresponding to axis, while np.append() does

a = np.array([[1,1],[2,2],[3,3]], int)
pprint(np.insert(a, 1, 5, axis=1))

a = np.array([[1,2,3],[4,5,6],[7,8,9]], int)
pprint(np.delete(a, 1, axis=0))

c = np.array([1,2,3], int)
pprint(c[np.newaxis, :])
pprint(c[:, np.newaxis])

# Creating ranges with (start, stop, [step]) syntax
print(np.arange(1,6,2, int))
print(np.arange(5, dtype=int))
print(np.arange(0,1.1,0.1, float))

# Create evenly spaced numbers over a specified interval
print(np.linspace(0, 5, num=3))

# Array mathematics is performed element-wise
a = np.array([[1,2],[3,4]], int)
print(a + b)
print(a * b)

### Creating matrices and vectors with zeros or ones ###
a = np.array([1,2,3], int)
a.fill(0)  #fill an existing array with a single value
pprint(np.ones((2,3),int))
print(np.zeros(7,int))
a = np.array([[1,2,3],[4,5,6]],int)
pprint(np.zeros_like(a))
pprint(np.ones_like(a))
pprint(np.identity(4,float))  # 4x4 matrix
pprint(np.eye(4,4,1,float))  # matrix with ones along the kth diagonal and zeros everywhere else

# Array broadcasting
a = np.zeros((2,2),float)
b = np.array([-1,3], float)
pprint(a + b[np.newaxis, :])
pprint(a + b[:, np.newaxis])

# Other useful functions
a = np.array([[1,2,1], [4,5,6], [7,8,7]], int)
print(a.diagonal())
print(np.unique(a))
b = np.array([6,2,5,-1,0], float)
print(b.clip(0,5))  # winsorize

# The np.digitize(x, bins, right=False) function
#
#   right   order of bins   returned index i satisfies
#-----------------------------------------------------
#   False   increasing          bins[i-1] <= x < bins[i]
#   True    increasing          bins[i-1] < x <= bins[i]
#   False   decreasing          bins[i-1] > x >= bins[i]
#   True    decreasing          bins[i-1] >= x > bins[i]

a = np.arange(100, dtype=int)
bins = np.arange(10, 101, 20, int)
print(np.digitize(a, bins))

### Vectorized Boolean operations ###
a = np.array([1,3,0], float)
print(np.where(a != 0, 1 / a, a))
b = np.logical_and(a > 0, a < 3)
c = np.logical_not(np.array([True,False,False], bool))
print(np.logical_or(b,c))

#### Checking for zeros, NANs and infinity ###
a = np.array([[0,2],[3,0]], float)
pprint(a.nonzero())
a = np.array([1, np.nan, np.inf, -np.inf], float)
a_finite = np.isfinite(a)
a_inf = np.isinf(a)
a_posinf = np.isposinf(a)
a_neginf = np.isneginf(a)
a_nan = np.isnan(a)

### Advanced array selection and manipulation ###
a = np.array([2,4,6,8], float)
b = np.array([0,0,1,3,2,1], int)  # position indices
print(a[b])  # the same can be done using lists
a = np.array([[1,4],[9,16]], float)
b = np.array([0,0,1,1,0], int)  # positions along first axis
c = np.array([0,1,1,1,1], int)  # positions along second axis
print(a[b,c])

a = np.array([[0,1],[2,3]], float)
b = np.array([0,0,1], int)
print(a.take(b, axis=0))
print(a.take(b, axis=1))
a = np.arange(0,6, dtype=float)
b = np.array([9,8,7], float)
a.put([0,3], b)
print(a)  # the third element of b is not used since only two positions were specified
a.put([0,3], 5)
print(a)  # the source array is broadcasted

### Numpy member functions ###
# - c.sum(), c.prod(), c.cumsum(), c.cumprod()
# - c.mean(), c.var(), c.std(), c.median()
# - c.min(), c.max(), c.argmin(), c.argmax()
# - c.quantile(), c.percentile(), c.ptp()
# All member functions have their standalone equivalents (e.g. np.sum(c), np.prod(c) etc)

# All member functions cannot handle NANs, but have their NAN-aware equivalents
# - np.nansum(), np.nanprod(), np.nanmin(), np.nanmax(), np.nanargmin(), np.nanargmax()
# - np.nanpercentile(), np.nanquantile(), np.nanmean(), np.nanstd(), np.nanmedian()
# - np.nanvar(), np.nancumsum(), np.nancumprod()

a = np.array([1,2,np.nan,3], float)
print(np.max(a))
print(np.nanmax(a))

# Applying member functions to a particular axis
a = np.array([[1,2,3],[4,5,6]], float)
print(a.mean(axis=0))
print(a.mean(axis=1))
print(a.ptp(axis=0))
print(a.ptp(axis=1))

### Sorting ###
# Note that c.sort() returns ndarray, while sorted(c) returns list
a = np.array([3,2,1], int)
print(sorted(a))
a.sort()
print(a)

### Numpy linalg submodule and basic linear algebra functions ###
# - np.dot(a,b) inner/dot product
# - np.outer(a,b) outer/tensor product
# - np.cross(a,b) cross/vector product
# - np.linalg.det(a) matrix determinant
# - np.linalg.inv(a) inverse matrix
# - np.linalg.eig(a) produces eigenvalues and eigenvectors
# - np.linalg.svd(a) singular value decomposition

### Set-like operations ###
a = np.array([1,2,3,4,5], int)
b = np.array([3,4,5,6,7], int)
print(np.intersect1d(a,b))
print(np.union1d(a,b))
print(np.setdiff1d(a,b))
print(np.setxor1d(a,b))
print(np.in1d(a,b))

# Vectorizing a user-defined function
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5))
factorial = np.vectorize(factorial)
print(factorial([1,2,3,4,5]))
print(factorial(np.arange(1, 10, 1)))

# A more elegant way using decorator
from numpy import vectorize
@vectorize
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial([1,2,3,4,5]))

### Numpy polynomial mathematics ###
coefs = [1,-4,4]
print(np.polyval(coefs, 2))  #evaluate a polynomial at a point
print(np.roots(coefs))  #find roots for a polynomial defined by a set of coefficients
p = np.poly([-1,1,1,10])  #show polynomial coefficients for a set of roots
p_derivative = np.polyder(p)  #derivative
p_integral = np.polyint(p)  #indefinite integral
# More polynomial arithmetics
# - np.polyadd(), np.polysub(), np.polymul(), np.polydiv()
# Fit a polynomial with OLS (order must be pre-specified)
# - np.polyfit(x,y,2)

