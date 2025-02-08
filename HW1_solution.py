### Euclidean Algorithm ###
def Euclidean(a, b):
    if (type(a) != int) or (type(b) != int):
        raise ValueError("The arguments must be of integer type")
    else:
        if a < b:
            a, b = b, a
        while True:
            q = a // b
            r = a - b * q
            if r == 0:
                break
            else:
                a, b = b, r
    return b


### Eratosthene's sieve ###
def Sieve(n):
    if (type(n) != int) or (n < 0):
        raise ValueError("The argument must be integer and a must be greater than 0")
    nums = [i for i in range(2, n + 1)]
    primes = []
    p = nums.pop(0)
    while p ** 2 <= n:
        primes.append(p)
        for i in range(p ** 2, n + 1, p):
            if i in nums:
                del nums[nums.index(i)]
        p = nums.pop(0)
    return primes + nums


### Merge sort ###
def merge(array1, array2):
    i = j = idx = 0
    result = list(array1 + array2)
    length = len(result)
    len1 = len(array1)
    len2 = len(array2)
    while idx < length:
        if j >= len2 or (i < len1 and (array1[i] < array2[j])):
            result[idx] = array1[i]
            i += 1
        else:
            result[idx] = array2[j]
            j += 1
        idx += 1
    return result


print(merge([1,2,3,7,8],[4,5,6]))


def mergesort(array):
    length = len(array)
    if length < 2:
        return array
    elif length == 2:
        if array[0] > array[1]:
            array[0], array[1] = array[1], array[0]
        return array
    else:
        pass
    result = array.copy()
    mid_idx = length // 2
    result = merge(mergesort(result[0:mid_idx]), mergesort(result[mid_idx:length]))
    return result


a = [3,8,2,7,1,5,4,6]
print(mergesort(a))


### Bubble sort ###
def bubblesort(array):
    n = len(array)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if array[i - 1] > array[i]:
                array[i - 1], array[i] = array[i], array[i - 1]
                swapped = True
    return array


### Fibonnacci numbers ###
def Fibonacci(n):
    if (type(n) != int) or (n < 0):
        raise ValueError("The argument must be positive integer")
    f1 = 1
    f2 = 1
    f_vec = [f1, f2]
    while (f1 + f2) < n:
        f_vec.append(f1 + f2)
        f1 = f_vec[-1]
        f2 = f_vec[-2]
    return f_vec


def CalculateSum(n):
    f_vec = Fibonacci(n)
    return sum(filter(lambda x: x % 2 == 0, f_vec))


print(CalculateSum(100))


### Recursive functions ###
def tetration(a, b):
    if type(b) != int:
        raise ValueError("The second argument must be integer")
    else:
        return a ** (tetration(a, b - 1)) if b else 1


def pentation(a, b):
    if type(b) != int:
        raise ValueError("The second argument must be integer")
    else:
        return tetration(a, pentation(a, b - 1)) if b else 1


def hyper(a, b, n):
    if type(n) != int or type(b) != int:
        raise ValueError("The second argument and the order of hyperoperator must be integers")
    elif n == 1:
        return a + b
    elif n == 2:
        return a * b
    elif n == 3:
        return a ** b
    else:
        return hyper(a, hyper(a, b - 1, n), n - 1) if b else 1


from operator import add, mul, pow
def hyper(a, b, n):
    if type(n) != int or type(b) != int:
        raise ValueError("The second argument and the order of hyperoperator must be integers")
    else:
        func_dict = {1: add, 2: mul, 3: pow}
        hyp = lambda x, y: hyper(x, hyper(x, y - 1, n), n - 1) if y else 1
        return func_dict.get(n, hyp)(a, b)


def reflect_seq(seq):
    return [*seq, *reversed(seq)]


def reflect_seq(seq, side = 'right'):
    if side == 'right':
        return [*seq, *reversed(seq)]
    elif side == 'left':
        return reflect_seq([*reversed(seq)])
    else:
        raise ValueError("The side must be either 'right' or 'left'!")


def super_reflect(seq):
    res = []
    for ls in seq[::-1]:
        res = [[*ls]] + res + [[*reversed(ls)]]
    return res


def recursive_reflect(seq, depth):
    res = []
    if depth == 0:
        res = [*seq, *reversed(seq)]
    elif depth == 1:
        for ls in seq[::-1]:
            res = [[*ls]] + res + [[*reversed(ls)]]
    else:
        for ls in seq[::-1]:
            res = [recursive_reflect([*ls], depth - 1)] + res + [recursive_reflect([*ls], depth - 1)]
    return res


def rotate_first(seq):
    return [*seq[1:], seq[0]]


def rotate_first(seq, side = 'right'):
    if side == 'right':
        return [*seq[1:], seq[0]]
    elif side == 'left':
        return [seq[-1], *seq[:-1]]
    else:
        raise ValueError("The side must be either 'right' or 'left'!")


from functools import reduce
def factorial(n):
    if type(n) != int or n < 0:
        raise ValueError("The argument must be a natural number")
    else:
        return reduce(mul, range(1, n + 1), 1)


def vfactorial(ls):
    check_zero = map(lambda x: x == 0, ls)
    check_type = map(lambda x: type(x) != int, ls)
    if any(check_zero) or any(check_type):
        raise ValueError("All elements of collection must be natural numbers")
    else:
        return list(map(factorial, ls))


ls = ['SOFT -> HARD -> None -> None',
      'SOFT -> HARD -> None -> SOFT',
      'HARD -> LEGAL - Field -> HARD -> None']

print(list(map(lambda w: ' -> '.join(filter(lambda x: x != 'None', w.split(' -> '))), ls)))


from itertools import permutations, combinations
def variations(ls, k):
    res = []
    combn = list(combinations(ls, k))
    for c in combn:
        p = list(permutations(c))
        res += p
    return res

