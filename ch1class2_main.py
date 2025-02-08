### Warm-up ###
def replace_nth(string, sub, rep, n):
	pos = string.find(sub)
	ind = (pos != -1)
	while pos != -1 and ind != n:
		pos = string.find(sub, pos + 1)
		ind += 1
	if ind == n:
		return string[:pos] + rep + string[pos + len(sub):]
	else:
		return string


str_foo = 'sssssss'
print(replace_nth(str_foo, 's', 'z', 5))
del str_foo

a = [1, 2, 3]
print(a.index(2))
# Returns the lowest index in list where the argument appears
print(a.index(2.0))

s = {'a', 'b', 'c'}
s.add('d')
d = {'a': 1, 'b': 2, 'c': 3}
d.pop('a')
d.popitem()

# The zip() function
x = [1, 2, 3]
y = [4, 5, 6]
z = zip(x, y)
print(type(z))
z = list(z)
print(z)
u, v = zip(*z)  # unzipping
print((u == tuple(x)) and (v == tuple(y)))


def cmp(a, b):
	if a == b:
		return 0
	elif a < b:
		return -1
	else:
		return 1


# Vectorizing cmp() function with zip()
a = [1, 2, 3]
b = [3, 2, 1]
c = [cmp(x, y) for (x, y) in zip(a, b)]
print(c)

# Creating a dict from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d_method1 = dict(zip(keys, values))
d_method2 = {key: val for (key, val) in zip(keys, values)}
print(d_method1, d_method2)

# Filtering a list with zip()
a_vec = [1, 2, 3, 4]
a_index = [True, False, False, True]
a_filtered = [x for (x,y) in zip(a_vec, a_index) if y]
for (x, y) in zip(a_vec, a_index):
	if y:
		a_filtered.append(x)
print(a_filtered)

### Functions ###
# A function may have a default value
# In this case, the function is evaluated when defined (not called!)
x0 = 10


def sqr(x=x0):
	return pow(x, 2)


print(sqr(3))
print(sqr())
print(sqr.__defaults__)
x0 = 25
print(sqr())

### Global and local variables ###
# 1. Standard variable hierarchy (no special keywords used)
x = 0


def outer_func():
	x = 1

	def inner_func():
		x = 2
		print("inner x: ", x)
	inner_func()
	print("outer x: ", x)


outer_func()
del x
# 2. With nonlocal keyword, inner function's x is also outer function's x
x = 0


def outer_func():
	x = 1

	def inner_func():
		nonlocal x
		x = 2
		print("inner x: ", x)
	inner_func()
	print("outer x: ", x)


outer_func()
print(x)
del x
# 3. With global keyword, inner function's x is bound to the global value
#global x
x = 0


def outer_func():
	x = 1

	def inner_func():
		global x
		x = 2
		print("inner x: ", x)
	inner_func()
	print("outer x: ", x)


outer_func()
print(x)
del x

# Functions are objects, too:

from math import sqrt, sin, cos, pi


def func_chooser(x, func = sin):
	return func(x)


print(func_chooser(pi / 2))
print(func_chooser(pi, cos))
print(func_chooser(sqrt(pi), sqr))

### Name binding in Python ###
a = [1, 2, 3, 4, 5]
b = a
a[1] = 100
print(b)

c = a.copy()
a[1] = 2
print(c)

del a, b, c

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = a.copy()
a[2][2] = 10
print(b)

from copy import deepcopy
c = deepcopy(a)
a[2][2] = 11
print(b)
print(c)

# Only mutable objects are subject to name binding
# Mutable: list, set, dict
# Immutable: int, float, str, tuple, bool, frozenset

# Hashing and hashable objects
keys = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
values = [sum(ls) for ls in keys]
d = dict(zip(keys, values))
# What went wrong?

# Only hashable objects can be keys for the dicts
# In order to be hashable, an object has to be immutable
print(hash(500))
print(hash('abcd'))
print(hash((1, 2, 3)))
print(hash({1, 2, 3}))  # error
print(hash(()))

# Empty data types
a = None
print(a is None)
print(type(a))
print(hash(a))


def empty_func():
	pass


b = empty_func()
print(b is None)

### The sys module ###
import sys
from pprint import pprint
pprint(sys.path)  # the paths where modules are imported from
# If you wish to import from another directory, add this command to your script:
new_path = 'C://Users//andrey.zakharov//py_training//scripts'  # path to your modules
if new_path not in sys.path:
	sys.path.append(new_path)

# System-specific information:
print(sys.platform)
print(sys.version)
print(sys.prefix)

# Size of Python objects in bytes
print(sys.getsizeof([1, 2, 3]))
print(sys.getsizeof(23.56))
print(sys.getsizeof([]))
print(sys.getsizeof(set()))
print(sys.getsizeof({}))

### Error handling ###
# The try-except-(else) statement catches errors of predefined type(s) and prevents code failure
while True:
	try:
		x = int(input("Please enter an integer >: "))
		break
	except ValueError:
		print("This is not a valid number. Please try again.")

# The finally statement is executed after the try-except-(else) statement regardless of whether an error was thrown or not
try:
	y = int(input("Please enter an integer >: "))
except ValueError:
	print("Sorry, this is not a valid number. Your answer was not processed.")
finally:
	print("Thank you!")


def safe_sort(array):
	try:
		array.sort()
	except AttributeError:
		pass
	return array


print(safe_sort([3, 2, 4, 1, 6, 5, 7, 9, 8]))
print(safe_sort('132'))


def sum_series(x, n):
	if abs(x - 1) < 1e-16:
		raise StopIteration
	x += 1 / (2 ** n)
	return x


x = 0
n = 1
while True:
	try:
		x = sum_series(x, n)
		n += 1
	except StopIteration:
		print(x)
		break


### Recursive functions ###
def factorial(n):
	if (type(n) != int) or (n < 0):
		raise ValueError("The argument must be integer")
	elif n == 0:
		return 1
	else:
		return n * factorial(n - 1)


print(factorial(5))
print(factorial(1.7))

print(factorial(900))
print(factorial(1000))
sys.setrecursionlimit(1500)
print(factorial(1000))

a = [5, 4, 7, 2, 1, 8, 6, 3, 9]


def quicksort(array):
	if len(array) < 2:
		return array
	else:
		lesser_array = []
		greater_array = []
		pivot = array[len(array) // 2]
		for x in array:
			if x < pivot:
				lesser_array.append(x)
			elif x > pivot:
				greater_array.append(x)
			else:
				continue
		return quicksort(lesser_array) + [pivot] + quicksort(greater_array)


print(quicksort(a))
