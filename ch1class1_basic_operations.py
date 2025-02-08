### Arithmetic operators and numeric types ###
a = 2
b = 3
print(type(a) == int)
print(type(a) == float)

print(a + b)
print(a * b)
print(a - b)
print(a ** b)
print(b / a)
print(b // a)

c = 2.0
print(type(c) == int)
print(type(c) == float)
print(c / b)
print(c // b)
d = int(c)
# Residual from integer division
print(b % d)
# Rounding
p = 3.247
print(round(p, 2))
q = round(p, 0)
print(type(q))

# Boolean operators
print(a == b)
print(a > b)
print(a < b)
print(a != b)

print((a <= b) or (a > b))
print((a <= b) and (a > b))
print(not ((a != b) or True))


def cmp(a, b):
	if a == b:
		return 0
	elif a < b:
		return -1
	else:
		return 1


print(cmp(4, 4))
print(cmp(4, 3))
print(cmp(3, 4))
print(cmp(4, 4.0))

# Complex numbers
w = 5 + 3j
print(w.real)
print(w.imag)

from math import floor, ceil
print(floor(3.8))
print(ceil(3.2))

### String and their operations ###
string_a = "aaa"
print(len(string_a))
string_b = "bbb"
string_c = string_a + string_b
print(string_c)
print("The new string has length %d" % len(string_c))  # C, Python 2
print("%s%s%s" % (string_a, string_b, string_c))
print("The new string has length {}".format(len(string_c)))  # Python 3
print(f"The new string has length {len(string_c)}")
print(2 * string_c)

str_long = 'supercalifragilisticexpialidocious'
print(str_long[0])
print(str_long[-1])
print(str_long[3:6])
print(str_long[2:10:2])
print(str_long[::3])
# Strings are immutable objects, so str_long[2] = 'z' will not work
print(str_long.replace('s', 'z', 1))
print(str_long.replace('s', 'z'))

print(str_long.find('exp', 0, len(str_long)))
str_cap = str_long.capitalize()
print(str_cap)
str_swp = str_cap.swapcase()
print(str_swp)
str_up = str_long.upper()
print(str_up)
str_low = str_up.lower()
print(str_low == str_long)
str_long += str_up
print(str_long)
print(''.join(sorted(str_long)))

message = "Hello how are you?"
print(message.split())
ind = 0
for word in message.split():
	ind += 1
	print("The word number %d is %s" % (ind, word))
	
s = " This string has extra spaces at ends  "
print(s.strip())

new_string = "a;b;c;d"
s = new_string.split(';')
add_string = ["e", "f"]
# Python 3 formatters
while len(s) != 6:
	elem = add_string.pop(0)
	s.append(elem)
	print("Adding: {}".format(elem))
	print("There are {} items in the string now".format(len(s)))
	
print(s)
print(s[1])
print(s[-1])
print(s.pop())
print(' '.join(s))
print('#'.join(s[2:4]))

vowels = 'aeiouy'
vowels_count = 0
for i in 'powerful':
	if i in vowels:
		vowels_count += 1

print(vowels_count)

vowels_count = 0
for i in vowels:
	vowels_count += 'powerful'.count(i)

print(vowels_count)

### Lists, sets, tuples and dictionaries ###
a = [1, 2, 3]
b = [4, 5, 6]
print(type(a))

# Concatenate and repeat lists
print(a + b)
print(a * 3)
# A simple generator expression
c = [i ** 2 for i in a] 

a.clear()
print(a)
del b[1]
print(b)
del b[:]
print(b)

del a, b, c

# List slicing: a[start:stop:step]
# Note that a[start:stop] includes start, but excludes stop, thus contains (stop-start) elements
str_list = ['red', 'blue', 'black', 'green', 'white']
print(str_list[3:])
print(str_list[:3])
print(str_list[::2])
print(str_list.count('red'))
print(str_list.count(str_list[3]))

# Add element to a list:
str_list.append('pink')
# Remove and return the last item
print(str_list.pop())
# Remove and return the first item
print(str_list.pop(0))

# Negative indexing denotes counting from the end
str_list.extend(['pink', 'purple'])
print(str_list[:-2])

# Reversing and sorting lists
list_rev = str_list[::-1]
list_reversed = list(reversed(str_list))
print(list_rev == list_reversed)
list_sorted = sorted(str_list)
# The same, but in-place
print(str_list.reverse())
print(str_list.sort())

num_list = list(range(-5,5))
list_inv = []
for elem in num_list:
	if elem == 0:
		continue
	list_inv.append(1 / elem)

print(list_inv)

# Boolean lists
bool_ls = [True, False, True]
print(any(bool_ls))
print(all(bool_ls))

# Tuples
a = [1, 2, 3]
a[2] = 5
b = tuple(a)
b[1] = 4
b = list(b)
b[1] = 4
a = (1, 2, 3)
print(type(a))

# Dictionaries
d = {'a': 1, 'b': 2, 'c': 3}
print(list(d.keys()))
print(list(d.values()))
print(list(d.items()))
d_inv = {val: key for (key, val) in d.items()}

d1 = {'p': 4, 'q': 5}
d.update(d1)
print(d)
d1.clear()
print(d1)
del d1

# Create dict without specifying strings as keys
d2 = dict(one=1, two=2, three=3)
print(d2)

ratings_moodys = {'Russia': 'Ba1', 'USA': 'Aaa', 'UK': 'Aa2', 'Ukraine': 'Caa2', 'Switzerland': 'Aaa', 'Venezuela': 'Caa3',
'China': 'A1', 'Canada': 'Aaa', 'Netherlands': 'Aaa', 'Brazil': 'Ba2', 'France': 'Aa2', 'India': 'Baa2', 'Pakistan': 'B3'}

print(ratings_moodys['Russia'])
ratings_moodys['Japan'] = 'A1'
print(ratings_moodys)
del ratings_moodys['Pakistan']

print('Canada' in ratings_moodys)
print('Kazakhstan' in ratings_moodys)

for key, val in sorted(ratings_moodys.items()):
	print('Country {} has rating {}'.format(key, val))

print(ratings_moodys.get('Zambia', 'This country is not rated'))
print(ratings_moodys.get('Brazil', 'This country is not rated'))

aggregation_moodys = {'Aaa': 'Aaa', 'Aa1': 'Aa', 'Aa2': 'Aa', 'Aa3': 'Aa', 'A1': 'A', 'A2': 'A', 'A3': 'A', 
'Baa1': 'Baa', 'Baa2': 'Baa', 'Baa3': 'Baa', 'Ba1': 'Ba', 'Ba2': 'Ba', 'Ba3': 'Ba', 'B1': 'B', 'B2': 'B', 'B3': 'B', 
'Caa1': 'Caa-C', 'Caa2': 'Caa-C', 'Caa3': 'Caa-C', 'Ca1': 'Caa-C', 'Ca2': 'Caa-C', 'Ca3': 'Caa-C', 'C': 'Caa-C'}

prob_transitions_moodys = {
'Aaa': {'Aaa': 96.90, 'Aa': 2.94, 'A': 0.04, 'Baa': 0.09, 'Ba': 0.00, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.04, 'D': 0.00},
'Aa': {'Aaa': 3.46, 'Aa': 92.91, 'A': 2.11, 'Baa': 0.79, 'Ba': 0.12, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.6, 'D': 0.00},
'A': {'Aaa': 0.00, 'Aa': 4.17, 'A': 91.22, 'Baa': 3.25, 'Ba': 1.29, 'B': 0.07, 'Caa-C': 0.00, 'WR': 0.00, 'D': 0.00},
'Baa': {'Aaa': 0.00, 'Aa': 0.00, 'A': 6.10, 'Baa': 89.10, 'Ba': 4.24, 'B': 0.51, 'Caa-C': 0.04, 'WR': 0.00, 'D': 0.00},
'Ba': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 8.32, 'Ba': 85.34, 'B': 5.33, 'Caa-C': 0.29, 'WR': 0.13, 'D': 0.58},
'B': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 4.76, 'B': 88.66, 'Caa-C': 3.47, 'WR': 0.41, 'D': 2.71},
'Caa-C': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 0.12, 'B': 17.83, 'Caa-C': 67.58, 'WR': 1.50, 'D': 12.97},
'D': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 0.00, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.00, 'D': 100.00}
}

transition_probs_rus = prob_transitions_moodys.get(aggregation_moodys[ratings_moodys['Russia']], 'NA')
print(transition_probs_rus.items())
print(transition_probs_rus['D'])

# Sets
a = {1, 2, 3}
b = set([0, 2, 4])
print(a - b)
print(a.difference(b))
print(a & b)
print(a.intersection(b))
print(a | b)
print(a.union(b))
print(a ^ b)  # symmetric diff

c = a & b
print(c.issubset(a))
print(a.issuperset(c))

# Check if all elements of list are the same
ls = ['a', 'a', 'a']
print(len(set(ls)) == 1)
print(all(x == ls[0] for x in ls))
print(ls.count(ls[0]) == len(ls))


### Functions ###
def double_it(x):
	return 2 * x


# Note that a function may have a default value
# In this case, the function is evaluated when defined (not called!)
x0 = 10


def double_it_mod(x=x0):
	return 2 ** x


x0 = 250
print(double_it_mod())

from math import sin, cos, exp, log, pi


def cos_solver(x=1.0):
	y = x
	for i in range(1000):
		y = cos(y)
	return y


print(cos_solver())


# Functions are objects, too
def func_chooser(x, func = sin):
	return func(x)


print(func_chooser(pi / 2))
print(func_chooser(pi, cos))
print(func_chooser(pi / 2, double_it))

# The zip() function
x = [1, 2, 3]
y = [4, 5, 6]
z = zip(x, y)
print(z)
u, v = zip(*z)  # unzipping
print(u)
print(v)

# Vectorizing cmp() function with zip()
a = [1, 2, 3]
b = [4, 5, 6]
c = [cmp(x, y) for (x, y) in zip(a, b)]
print(c)

# Creating a dict from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d_method1 = dict(zip(keys, values))
d_method2 = {key:val for (key, val) in zip(keys, values)}
print(d_method1, d_method2)

# Filtering a list with zip()
a_vec = [1, 2, 3, 4]
a_ind = [True, False, False, True]
a_refined = [x for (x, y) in zip(a_vec, a_ind) if y]
print(a_refined)

# Name binding
a = [1, 2, 3, 4, 5]
b = a
a[1] = 100
print(b)

c = a.copy()
a[1] = 2
print(c)

# Only mutable objects are subject to name binding
# Mutable: list, set, dict
# Immutable: int, float, str, tuple, bool, frozenset

keys = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
values = [sum(ls) for ls in keys]
d = dict(zip(keys, values))
# What went wrong?

# Only hashable objects can be keys for the dicts
# In order to be hashable, an object has to be immutable
print(hash(500))
print(hash(42000000000))
print(hash('abcd'))
print(hash((1, 2, 3)))
print(hash({1, 2, 3}))  # error

# Empty data types
a = None
print(a is None)
print(type(a))
print(hash(a))


def empty_func():
	pass


b = empty_func()
print(b is None)
