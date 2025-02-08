### Warm-up ###

a = [1, 2, 3, 4]
b = [True, False, False, True]
c = [x for (x, y) in zip(a, b) if y]
c = [x if y else 0 for (x, y) in zip(a, b)]
print(c)

### Map, filter, reduce, accumulate ###
from math import exp
from operator import *
from functools import reduce
from itertools import *

vec = list(range(0, 10))
# Apply a function to a list of inputs
vec_exp = map(exp, vec)
print(list(vec_exp))
# Note that map() returns a list in Python 2, and a 'map object' in Python 3

vec += [-x for x in vec]


# Create a subset of list elements as another list, for which the function returns True
def natural_num(x):
	return (x > 0) and (type(x) == int)


vec_nat = filter(natural_num, vec)
print(list(vec_nat))
# Note that filter() also returns a special 'filter object' that needs to be converted for display

vec = [2, 2, 3, 2]
print(reduce(pow,vec))
print(list(accumulate(vec, pow)))
# Again, note that accumulate() returns an 'accumulate object'

a_numeric = [-1, 1, 2, 0, 0, -2, 0]
a_logical = list(map(bool, a_numeric))
print(a_logical)

# Standard operators as functions:
# lt(a,b) <=> a < b
# gt(a,b) <=> a > b
# eq(a,b) <=> a == b
# ne(a,b) <=> a != b
# le(a,b) <=> a <= b
# ge(a,b) <=> a >= b
# add(a,b) <=> a + b
# sub(a,b) <=> a - b
# mul(a,b) <=> a * b
# pow(a,b) <=> a ** b
# div(a,b) <=> a / b
# mod(a,b) <=> a % b
# floordiv(a,b) <=> a // b
# and_(a,b) <=> a and b
# or_(a,b) <=> a or b

print(list(accumulate(a_numeric, sub)))
print(reduce(or_, a_logical))
print(list(accumulate(a_logical, and_)))

# Other itertools utilities
# Compress, chain, count, repeat, cycle
a = [1, 2, 3, 4]
b = [True, False, False, True]
print(list(compress(a, b)))
print(list(compress('ABCDEF', [1, 0, 1, 0, 1, 1])))
c = chain('ABC', 'DEF')
for i in range(6):
	print(next(c))
print(list(c))
c = chain('ABC', 'DEF', [1, 2, 3], {True, False}, ('a', 'b', 'c'))
while True:
	try:
		print(next(c))
	except StopIteration:
		break
print(list(c))
count1 = count(10)
count2 = count(11, 2)
k = 0
while True:
	n1 = next(count1)
	n2 = next(count2)
	k += 1
	if (n2 % 3) == (n1 % 3):
		print((n1, n2))
		print("Condition satisfied at step %d" % k)
		break
	else:
		print(k)

print(list(repeat([1, 2, 3, 4], 3)))
a = [1, 2, 3, 4]
c = cycle(a)
print(next(c))

# Combinations and permutations
print(list(permutations('ABCD')))
print(list(permutations([1, 2, 3, 4])))
print(list(combinations('ABCD', 2)))
print(list(combinations([1, 2, 3, 4], 3)))

# Starmap
ls = [(2, 5), (3, 2), (10, 3)]
print(list(starmap(pow, ls)))
# Note that in Python 2, the itertools module has additional functions izip(), imap(), ifilter()
# However, the Python 2 itertools module does not support accumulate()

### Built-in utilities for random number generation ###
import random
print(random.randrange(0, 10))
print(random.random())  # next random float in [0,1)
vec = list(range(10))
print(random.choice(vec))
print(vec)
random.shuffle(vec)
print(vec)
print(random.sample(vec,3))

### Anonymous functions ###
vec = range(10)
vec_sqr = map(lambda x: x ** 2, vec)
print(list(vec_sqr))
nums = range(-5, 5)
print(list(map(lambda x: 1 / x, filter(lambda x: x != 0, nums))))

# itertools' takewhile and dropwhile functions
print(list(takewhile(lambda x: x > 0, [1, -2, 3, -3])))
print(list(dropwhile(lambda x: x > 0, [1, -2, 3, -3])))

PD_marg = [0.017, 0.033, 0.048, 0.061, 0.072, 0.082, 0.09, 0.097, 0.103, 0.108, 0.113, 0.118, 0.119, 0.12, 0.12]
PD_cumm = accumulate(PD_marg, lambda x, y: 1 - (1 - x) * (1 - y))
print(list(PD_cumm))

# Recall: functions are objects, too
funcs = [mul, add]
for (i, j) in zip(range(5), range(5)):
	value = map(lambda x: x(i, j), funcs)
	print(tuple(value))


def powerbase(n):
	return lambda x: n ** x


p2 = powerbase(2)
print(p2(3))

sentence = 'Python is a very expressive programming language'
words = sentence.split(' ')
lengths = list(map(lambda w: len(w), words))

# Sort dict by value
d = {'a': 4, 'b': 3, 'c': 2, 'd': 1}
# Method 1
print(list(sorted(d.items(), key=lambda x: x[1])))
# Method 2
print(list(sorted(d.items(), key=itemgetter(1))))

# Anonymous functions can also have a default value for argument
res1 = (lambda x=2: x ** 2)()
print(res1)
res2 = (lambda x=2: x ** 2)(4)
print(res2)

### Smart collections ###
from collections import OrderedDict, namedtuple

# Ordered dicts
ord_dict = OrderedDict.fromkeys('abcde')
print(ord_dict)
ord_dict.move_to_end('b')
print(''.join(ord_dict.keys()))
ord_dict.move_to_end('b', last = False)
print(''.join(ord_dict.keys()))
ord_dict.popitem(last=True)
# dict sorted by key
d_keysort = OrderedDict(sorted(d.items(), key=lambda x: x[0]))
# dict sorted by val
d_valsort = OrderedDict(sorted(d.items(), key=lambda x: x[1]))
# dict sorted by length of the key string
d_lensort = OrderedDict(sorted(d.items(), key=lambda x: len(x[0])))

# Named tuples
tup = namedtuple('ntuple', ['x', 'y'])
print(type(tup))
t = tup(2, y=3)
print(type(t))
print(t[0] + t[1])
print(t.x + t.y)
print(t._fields)
t.y = 4  # error
t._replace(y=4)
d = t._asdict()
print(type(d))
ls = [1, 2]
t1 = tup._make(ls)
x, y = t
print(x, y)
