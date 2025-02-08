### Warm-up ###
import sys
import math
from itertools import cycle, chain, product, islice
from functools import total_ordering
from collections import deque
from pprint import pprint

a = [1, 2, 3]
b = 'abcd'
print(list(product(a, b)))

c = cycle([1, 2, 3])
print(next(c))
c = chain([1, 2, 3], 'abc')
print(next(c))


def my_cycle(coll):
    n = len(coll)
    i = 0
    while True:
        if i == n:
            i = 0
        yield coll[i]
        i += 1


c = my_cycle([1, 2, 3])
print([next(c) for _ in range(10)])


def my_chain(*colls):
    for coll in colls:
        for i in range(len(coll)):
            yield [*coll][i]


c = my_chain([1, 2, 3], 'abc', {4, 5})
print(next(c))


def cycle_chain(*colls):
    ls = []
    for coll in colls:
        ls += [*coll]
    yield from my_cycle(ls)


c = cycle_chain([1, 2, 3], 'abc', {4, 5}, (6, 7, 8))
print([next(c) for _ in range(30)])

# Exploring deque objects (double-ended queues)
a = [1, 2, 3]
dq = deque(a, 5)
print(dq)
# Syntax: deque(iterable, maxlen)
# "maxlen" is an optional argument; if specified, adding elements to a full deque will discard
# a corresponding number of items from the opposite end
dq.append(4)
print(dq)
dq.appendleft(5)
print(dq)
dq.rotate(1)  # take one element from right side and append it to the left
print(dq)
dq.rotate(-2)  # take two elements from left side and append it to the right
print(dq)
# Rotation can be recreated with .pop() and .append() methods:
dq.appendleft(dq.pop())
print(dq)
dq.append(dq.popleft())
print(dq)
ls = [0]
dq.extendleft(ls)
print(dq)
# The .insert(i, x) method works for unbounded deques, but raises an IndexError for bounded ones
# Deque objects also support .extend(), .clear(), .remove(x), .reverse() and .count(x) methods
# These methods work exactly as in lists

# Treating slices as objects
a = list(range(10))
s = slice(1, 7)
print(s)
print(type(s))
print(a[s])
print(s.start, s.stop, s.step)

s = islice(a, 4)  # part of collection as an independent object
print(a[s])  # does not work since islice() is not a slice(), but rather an already sliced object
print(list(s))
print(deque(s))  # islice() is an iterator, so repeated use is impossible

### Introduction to object-oriented programming ###
# Relationship between classes and instances
print(isinstance([1, 2, 3], list))
print(isinstance('abc', str))
print(isinstance(2.0, int))


# Creating custom classes
class Foo1(object):
    class_info = "The Foo1 class was created for training."  # this is class attribute

    def __init__(self, val):
        self.value = val  # this is instance attribute

    def sqr(self):
        return self.value ** 2


foo = Foo1(4)
print(foo.__class__)
print(type(foo) is foo.__class__)  # in Python class and type are always the same
print(isinstance(foo, Foo1))
print(hasattr(foo, 'sqr'))
print(hasattr(foo, 'value'))
print(hasattr(foo, 'class_info'))
print(foo.value)
print(foo.sqr())
print(hasattr(Foo1, 'class_info'))
print(Foo1.class_info)
# Accessing the attribute namespace of objects
print(foo.__dict__)  # only attributes are included in dict (not methods)
print(Foo1.__dict__)

# Dynamic attribute creation
foo.x = 2
print('x' in foo.__dict__)
setattr(foo, 'y', 3)
print('y' in foo.__dict__)
del foo.x
print(foo.x)  # AttributeError
delattr(foo, 'y')
print('y' in foo.__dict__)

pprint(sys.modules[__name__].__dict__)  # namespace of the current module!

# Exploring namespaces
# - globals() always returns the __dict__ of the module namespace
pprint(globals())
# - locals() always returns the __dict__ of the current namespace
# Note that locals() behaves differently for functions and other objects


class Foo(object):
    a = 1
    b = 2
    var_dict = locals()
    c = 3
    pprint(var_dict)
    var_dict['d'] = 4
    pprint(var_dict)


print(Foo.d)


def func():
    a = 1
    b = 2
    var_dict = locals()
    c = 3
    print(var_dict)  # c is not in dict
    var_dict['d'] = 4
    print(var_dict)  # d is in dict
    print(d)  # but d is not defined!


func()

# Note that var_dict contains itself as value (i.e. it is a recursive dict)
# - vars() returns either the __dict__ of the current namespace or the __dict__ of its argument
print(vars(foo))
print(vars(Foo1))


# Introduction to inheritance
class Foo2(object):
    pass


foo = Foo2()  # but how is it possible if Foo2 class does not have an __init__() method?
print(foo.__dict__)  # empty
# Some built-in Python objects also do not have a __dict__ attribute:
print([].__dict__)

# Exploring dir()
print(dir([]))
# The dir() function uses not only __dict__ of instance and its class,
# but also the __dict__ of instance's base class (in our case, this is 'object' class)
print(dir(foo))
print(issubclass(Foo2, object))
print(dir())  # namespace of the current module
print(dir(dir))  # namespace of dir() itself

# Delete all user-created variables in module:
# Method 1
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
# Method 2
module = sys.modules[__name__]
for name in dir():
    if not name.startswith('_'):
        delattr(module, name)

# Exploring 'object' class
o = object()
print(o.__dict__)  # error
print(dir(o))
# Note the following methods: __dir__(), __eq__(), __gt__(), __ge__(), __lt__(), __le__(),
# __ne__(), __hash__(), __str__(), __repr__(), __init__(), __new__()
# Methods that define the behavior of object as argument for built-in functions
# are called 'dunder' methods (because of double underscores __).
# NOTE: the Foo2 class has inherited these methods from 'object' class

print(o == o)  # behavior defined by __eq__() method
print(hash(o))  # behavior defined by __hash__() method
# 'object' is the most basic class in Python - all other classes are derived from it
print(issubclass(object, object))


### Inheritance and override: a toy example ###
class Parent(object):
    def hello(self):
        print("Hello!")

    def goodbye(self):
        print("Goodbye!")


p = Parent()
print(isinstance(p, Parent))
p.hello()
p.goodbye()


# The Child class inherits hello() method and overrides goodbye() method
class Child(Parent):
    def goodbye(self):
        print("Goodbye for now, but I'll be back!")


c = Child()
print(isinstance(c, Child))
print(isinstance(c, Parent))
print(issubclass(Child, Parent))
c.hello()
c.goodbye()

# The GrandChild class inherits hello() method and modifies goodbye() method
import time


class GrandChild(Child):
    def goodbye(self, n=5):
        print("I have to go...")
        super(GrandChild, self).goodbye()  # Python 2 style (but the syntax is valid in Python 3)
        time.sleep(n)
        print("Hello again!")


g = GrandChild()
print(issubclass(GrandChild, Child))
print(issubclass(GrandChild, Parent))
g.hello()
g.goodbye()


### Composition: a toy example ###
class Friend(object):
    def __init__(self):
        self.buddy = GrandChild()

    def hello(self):
        self.buddy.hello()

    def goodbye(self, k=10):
        print("My friend says:")
        self.buddy.goodbye(k)
        print("I made him absent for %d sec instead of what he was used to" % k)


f = Friend()
print(issubclass(Friend, Child))
f.hello()
f.goodbye(8)


# Another example: using super() with __init__()
class Rectangle(object):
    def __init__(self, a, b):
        self.height = a
        self.width = b

    def CalculatePerimeter(self):
        return 2 * self.width + 2 * self.height

    def CalculateArea(self):
        return self.height * self.width


class Square(Rectangle):
    def __init__(self, a):
        super().__init__(a, a)  # Python 3 style


s = Square(8)
print(s.CalculatePerimeter())
print(s.CalculateArea())


# Static and class methods
class Foo(object):
    def plain_method(self):
        return "Instance method called", self

    @classmethod
    def class_method(cls):
        return "Class method called", cls

    @staticmethod
    def static_method():
        return "Static method called"


foo = Foo()
foo.plain_method()
foo.class_method()  # instance has access to its class methods
foo.static_method()
Foo.plain_method()  # class does not have access to its instances' methods
Foo.class_method()
Foo.static_method()


# Example of static method:
class Circle(object):
    def __init__(self, rad):
        self.r = rad

    def CalculateLength(self, imply_pi=False):
        if imply_pi:
            pi = self.ApproximatePi(1000)
        else:
            pi = math.pi
        self.length = 2 * pi * self.r
        return self.length

    def CalculateArea(self, imply_pi=False):
        if imply_pi:
            pi = self.ApproximatePi(1000)
        else:
            pi = math.pi
        self.area = pi * self.r ** 2
        return self.area

    @staticmethod
    def ApproximatePi(n):
        res = 1
        for i in reversed(range(3, n, 2)):
            res = 6 + i ** 2 / res
        return 3 + 1 / res


c = Circle(5)
pi_ = c.ApproximatePi(1000)
print(c.CalculateLength())
print(c.CalculateLength(imply_pi=True))
print(c.CalculateArea())
print(c.CalculateArea(imply_pi=True))


### The general notion of an iterator ###
a = [1, 2, 3]
print(next(a))  # error
b = iter(a)
print(next(b))  # len(a) + 1 times

# An object is called iterable if we can get an iterator from it
# Most of built-in containers in Python (list, tuple, str, set) are iterables


# Moving average iterator
def mov_avg(iterable, n=5):
    it = iter(iterable)
    dq = deque(islice(it, n - 1))
    dq.appendleft(0)
    s = sum(dq)
    for elem in it:
        s += elem - dq.popleft()
        dq.append(elem)
        yield s / n


x = range(10)
x_ma = mov_avg(x)
print(next(x_ma))


# Building an iterable object
class Fibonacci(object):
    def __init__(self):
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):

        return self

    def __next__(self):
        a, self.n, self.a, self.b = self.a, self.n + 1, self.b, self.a + self.b
        return a


# The __iter__() and __next__() methods are sometimes referred to as the 'iterator protocol'
fib = Fibonacci()
print([next(fib) for _ in range(20)])

# However, a basic iterator does not support item extraction (e.g. fib[0] or [i for i in fib]
# The __getitem__() and __len__() methods define the 'sequence protocol'
# Clearly, list and tuple are sequences (because they are ordered collections)
# But set is not a sequence since it is not ordered
s = {1, 2, 3}
print(s[0])  # TypeError


# Building a sequence object
class Fibonacci(object):
    def __init__(self):
        self.n, self.a, self.b = 0, 0, 1

    def __move_next(self):
        a, self.n, self.a, self.b = self.a, self.n + 1, self.b, self.a + self.b
        return a

    def __getitem__(self, m):
        self.__init__()
        while m > self.n:
            self.__move_next()
        else:
            res = self.a
            return res

    def __len__(self):
        return self.n + 1


fib = Fibonacci()
print([fib[9], fib[10], fib[3]])
print(len(fib))
# But slicing is still impossible
print(fib[1:3])  # error
# Task: try slice() or islice() to write a Fibonacci sequence that supports slicing

# Python's 'private' methods
print(fib.__move_next())  # AttributeError
print('__move_next' in fib.__dict__)
pprint(dir(fib))
# Note: the name of 'private' method '__move_next' has been changed to '_Fibonacci__move_next'
# The '__Method' are not truly private methods: they are used only to avoid confusion when
# inheriting from classes that have methods with the same name


# Creating custom error types
class FinancialError(Exception):
    def __init__(self):
        super().__init__("The inputs provided violate economic or business logic")


# Overriding built-in functions with dunder methods
@total_ordering
class Debt(object):
    def __init__(self, total_debt, *, principal, interest=None):
        self.total_debt = total_debt
        self.principal = principal
        if interest is None:
            interest = total_debt - principal
        else:
            try:
                assert principal + interest <= total_debt
            except AssertionError as err:
                raise FinancialError() from err
        self.interest = interest

    def __lt__(self, other):
        return self.total_debt < other.total_debt

    def __eq__(self, other):
        return self.total_debt == other.total_debt


d1 = Debt(total_debt=10000, principal=9000)
d2 = Debt(total_debt=9900, principal=9100)
print(d1 <= d2)
print(d1 > d2)
print(d1 != d2)

# In order to use total_ordering decorator, the class must supply the __eq__() method and
# one or more comparison ordering methods __lt__(), __le__(), __gt__() or __ge__()

d3 = Debt(total_debt=10000, principal=7000, interest=4000)  # error
try:
    d3 = Debt(total_debt=10000, principal=7000, interest=4000)
except FinancialError as e:
    print(e.__cause__.__class__)

import numpy as np


class custom_nan(object):
    def __init__(self):
        pass

    def __str__(self):
        return "object of type '<custom nan>'"

    def __repr__(self):
        return "Custom NaNs are objects with properties similar to those of np.nan, but with re-concidered interaction with objects of np.inf class"

    def __gt__(self, other):
        if np.isneginf(other):
            return True
        else:
            return False

    def __lt__(self, other):
        if np.isposinf(other):
            return True
        else:
            return False

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __ge__(self, other):
        return bool(self.__gt__(other) + self.__eq__(other))

    def __le__(self, other):
        return bool(self.__lt__(other) + self.__eq__(other))

    def __add__(self, other):
        if np.isinf(other):
            return other
        else:
            return self

    def __radd__(self, other):
        if np.isinf(other):
            return other
        else:
            return self

    def __sub__(self, other):
        if np.isneginf(other):
            return np.inf
        elif np.isposinf(other):
            return -np.inf
        else:
            return self

    def __rsub__(self, other):
        if np.isposinf(other):
            return np.inf
        elif np.isneginf(other):
            return -np.inf
        else:
            return self

    def __mul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        if np.isinf(other):
            return 0.0
        else:
            return self

    def __rtruediv__(self, other):
        if np.isinf(other):
            return other
        else:
            return self

    def __pow__(self, exponent):
        return self

    def __rpow__(self, base):
        return self


my_nan = custom_nan()
print(my_nan)
repr(my_nan)
print(my_nan + np.inf)
print(my_nan - np.inf)
print(my_nan < np.inf)
print(my_nan == my_nan)
