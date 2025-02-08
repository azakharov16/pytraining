### Python riddles ###

# 1
# How to check if the list is empty?
a = []
if len(a) == 0:
	print("The list is empty.")
if not a:
	print("The list is empty.")
print(not [])
print(not {})
# "Assuming the implicit booleanness of an empty list is quite Pythonic"
print(bool(""))
print(bool([{}]))
print(bool([1, 2, 3]))
print(not set())
print(not frozenset())
print(bool(None))


# Official equivalent of the cmp() function
def cmp(x, y):
	return (x > y) - (x < y)


# 2
print([] or None)
print(None or [])
print([] is None)
# Explanation: x = y or z is an idiom equivalent to x = y if y else z

# 3
d = {True: 'yes', 1: 'no', 1.0: 'maybe'}
print(d)

# 4
x = [[1, 2, 3, 4, 5]] * 3
y = [[1, 2, 3, 4, 5] for _ in range(3)]
# What's the difference?
x[0][3] = 10
print(x)
y[0][3] = 10
print(y)

# 5
a = 1
b = 2
# Task: swap values of a and b

# 6
print([1, 2, 3] is [1, 2, 3])
print([] is [])
print({} is {})
print(None is None)

# 7
a = [1, 2, 3]
b = a
print(a == b)
print(a is b)
c = list(a)
print(a == c)
print(a is c)


# 8
def func(arg=[]):
	arg.append('x')
	return arg


print(func())
print(func())

# The use of star operators
print(sum(2, 3))  # error


def mysum(*nums):
	return sum([*nums])


print(mysum(2, 3, 5, 6))


def IntroduceMyself(**data):
	for (key, val) in data.items():
		print("My {} is {}".format(key, val))
	return None


IntroduceMyself(name='Andrey', department='Advisory', team='FSRM', grade='Senior')

nums =[1, 2, 3]
nums = [*nums, 4, 5]
print(*nums, sep=';')


def transpose(mat):
	return [list(row) for row in zip(*mat)]


from pprint import pprint
m = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
pprint(transpose(m))

date_info = {'year': '2019', 'month': '04', 'day': '25'}
filename = "{year}-{month}-{day}.txt".format(**date_info)
print(filename)

# Both * and ** can be used several times in a function call, but the required order is func(fargs, *args, **kwargs)
cols = ['blue', 'red', 'white']
print(*nums, *cols)

author_info = {'name': 'Andrey', 'team': 'FSRM'}
filename = "{year}-{month}-{day}-{name}-{team}.txt".format(**date_info, **author_info)
print(filename)


def get_multiple(*keys, d, default=None):
	return [d.get(key, default) for key in keys]


fruits = {'lemon': 'yellow', 'peach': 'red', 'apple': 'green', 'plum': 'purple'}
print(get_multiple('lemon', 'apple', 'pear', d=fruits, default='unknown'))

ls = [1, 2, 3, 4, 5]
one, two, *remaining = ls
print(remaining)
one, *middle, five = ls
print(middle)

# Nested extraction
fruits = ['lemon', 'apple', 'peach']
((first, *remaining), *other_fruits) = fruits
print(remaining)

# The * operator works with any iterable object, while + works with only some types of iterables
# (and both arguments must be of the same type!)
fruits_more = ('melon', 'pear')
fruit_set = {*fruits, *fruits_more}

all_info = {**date_info, **author_info}
event_info = {**all_info, 'room':'P240'}


# Forcing keyword arguments
def mycrazysum(a, b, *, c=1, d=2):
	return mysum(a, b, c, d)


s = mycrazysum(0, 1, 2, 3)
s = mycrazysum(0, 1, c=2, d=3)

# TASKS
# Reflect list using *
# Rotate first element of list using *
