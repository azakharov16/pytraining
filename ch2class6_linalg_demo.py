### Warm-up ###
import numpy as np
import scipy as sp
import datetime as dt
from pprint import pprint
# from matplotlib import pyplot as plt

a = [1, 2, 3, np.nan]
b = [np.nan, 1, 2, 3]
print(max(a))
print(max(b))
print(np.nanmax(a))
print(np.nanmax(b))
# Note that the occurrence of np.nan in a list or ndarray forces its elements to float type

# Numpy datetime functions
d = np.datetime64('2019-05-15')
d_str = np.datetime_as_string(d)
d_dt = d.astype(dt.datetime)

date_arr = np.array(['2017-12-31', '2016-12-31', '2015-12-31'], dtype='datetime64')
drange = np.arange(d_str, '2020-05-15', dtype='datetime64')

print(np.datetime_data(d))  # information about step size of a date object
print(np.datetime64('2015-10', 'D'))  # defaults to the first day of month

# Poissible types for datetime range:
# dtype = 'datetime64[s]' seconds
# dtype = 'datetime64[m]' minutes
# dtype = 'datetime64[h]' hourly
# dtype = 'datetime64[D]' daily (also by default)
# dtype = 'datetime64[w]' weekly
# dtype = 'datetime64[M]' monthly
# dtype = 'datetime64[Y]' yearly

a = np.array([[1,2], [3,4]], int)
for i, val in np.ndenumerate(a):
    print((i, val))

b = np.array([[5,6],[7,8]], int)
pprint(np.stack((a, b), axis=0))
pprint(np.stack((a, b), axis=1))
pprint(np.hstack((a, b)))
pprint(np.vstack((a, b)))
pprint(np.dstack((a, b)))

### Linear algebra examples ###

# Numerical solution of linear systems with Jacobi method
def jacobi(A, b, n=25, x=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    if x is None:
        x = np.zeros(len(A[0]))
    # Create a vector of the diagonal elements of A and subtract them from A
    D = np.diag(A)
    R = A - np.diagflat(D)
    # Iterate for N times
    for i in range(n):
        x = (b - np.dot(R, x)) / D
    return x

A = np.array([[2.0,1.0],[5.0,7.0]], float)
b = np.array([11.0,13.0], float)
guess = np.array([1.0,1.0], float)
solution = jacobi(A, b, n=25, x=guess)
print(solution)

# Cholesky decomposition with scipy
A = np.array([[6, 3, 4, 8], [3, 6, 5, 1], [4, 5, 10, 7], [8, 1, 7, 25]], float)
L = sp.linalg.cholesky(A, lower=True)
pprint(L)
pprint(np.dot(L, L.T))  # check
U = sp.linalg.cholesky(A, lower=False)
pprint(U)
pprint(np.dot(U.T, U))  # check

# LDL decomposition with scipy
A = np.array([[6, 3, 4, 8], [3, 6, 5, 1], [4, 5, 10, 7], [8, 1, 7, 25]], float)
L, D, P = sp.linalg.ldl(A, lower=True)
pprint(L)
pprint(D)
pprint(np.dot(L, np.dot(D, L.T)))  # check
U, D, P = sp.linalg.ldl(A, lower=False)
pprint(U)
pprint(D)
pprint(np.dot(U, np.dot(D, U.T)))  # check

# LU decomposition with scipy
A = np.array([[7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6]], float)
P, L, U = sp.linalg.lu(A)
pprint(L)
pprint(U)
pprint(np.dot(L, U))  # check

# QR decomposition with scipy
A = np.array([[12, -51, 4], [6, 167, -68], [-4, 24, -41]], float)
Q, R = sp.linalg.qr(A)
pprint(R)
pprint(sp.allclose(np.identity(3, float), np.dot(Q.T, Q)))
pprint(np.dot(Q, R))  # check

# np.allclose(a, b, rtol=1e-05) is the numpy equivalent
# The function returns True if the two arrays are element-wise equal within a given tolerance level
