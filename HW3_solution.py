from math import sqrt
import random


def mean(x_vec):
    return sum(x_vec) / len(x_vec)


def std(x_vec):
    x_bar = mean(x_vec)
    n = len(x_vec)
    x_sqr = [x ** 2 for x in x_vec]
    return sqrt((sum(x_sqr) - n * x_bar ** 2) / (n - 1))


def jackknife(x_vec, func):
    param_vec = []
    for i in range(len(x_vec)):
        x_cut = x_vec[:i] + x_vec[(i + 1):]
        param_vec.append(func(x_cut))
    return mean(param_vec)


def bootstrap(x_vec, func, nrep):
    param_vec = []
    n = len(x_vec)
    for _ in range(nrep):
        param_vec.append(func(random.choices(x_vec, k=n)))
    return mean(param_vec), std(param_vec)


random.seed(1234)
a = 5.0
b = 10.0
v = [random.uniform(a, b) for _ in range(10000)]
print((a + b) / 2)
print((b - a) / sqrt(12))
print(mean(v))
print(std(v))
print(jackknife(v, mean))
print(jackknife(v, std))
print(bootstrap(v, mean, 10000))
print(bootstrap(v, std, 10000))

