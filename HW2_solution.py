import sys
from math import sin, pi
from functools import partial
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

path_yfrac = 'C://Users//Andrey.Zakharov//PycharmProjects//training//class5'
sys.path.append(path_yfrac)
from yearfrac import yearfrac

# Vectorizing dict's .get() method
a = np.array([1, 2, 3, 4, 5], int)
d = {1: 'one', 2: 'two', 3: 'three', 6: 'six'}
print(np.vectorize(d.get)(a).tolist())
print(np.vectorize(lambda x: d.get(x, 'NA'))(a).tolist())


# Method 1
def kramer_solve(a_mat, b_vec):
    if a_mat.shape[0] != a_mat.shape[1]:
        raise ValueError("The coefficient matrix must be square")
    a_det = np.linalg.det(a_mat)
    if a_det == 0:
        raise ValueError("The coefficient matrix is singular")
    x_vec = []
    for i in range(len(b_vec.tolist())):
        a_mod = np.concatenate((a_mat[:, :i], b_vec[:, np.newaxis], a_mat[:, (i + 1):]), axis=1)
        x = np.linalg.det(a_mod) / a_det
        x_vec.append(x)
    return np.array(x_vec)


A = np.array([[2.0, 1.0], [5.0, 7.0]], float)
b = np.array([11.0, 13.0], float)
solution1 = kramer_solve(A, b)
print(solution1)


# Method 2
def kramer_solve(a_mat, b_vec):
    if a_mat.shape[0] != a_mat.shape[1]:
        raise ValueError("The coefficient matrix must be square")
    a_det = np.linalg.det(a_mat)
    if a_det == 0:
        raise ValueError("The coefficient matrix is singular")
    x_vec = []
    for i in range(len(b_vec.tolist())):
        a_mod = np.delete(np.insert(a_mat, i, b_vec, axis=1, ), i + 1, axis=1)
        x = np.linalg.det(a_mod) / a_det
        x_vec.append(x)
    return np.array(x_vec)


solution2 = kramer_solve(A, b)
print(solution2)


# Numeric integration
def integrate(func, a, b, n=1000):
    delta = (b - a) / n
    x_seq = [a + delta * i for i in range(n + 1)]
    y_seq = list(map(func, x_seq))
    y_sum = [(y1 + y2) / 2 for (y1, y2) in zip(y_seq[:-1], y_seq[1:])]
    return sum(y_sum) * delta


print(integrate(sin, 0, pi))


def integrate_np(func, a, b, n=1000):
    x_seq = np.linspace(a, b, num=n)
    func = np.vectorize(func)
    y_seq = func(x_seq)
    return np.trapz(y_seq, x_seq)


print(integrate_np(np.sin, 0, np.pi))

# Simulation
np.random.seed(12345)


def prepare_tenors(start_date, end_date, *, func=yearfrac):
    drange = np.arange(start_date, end_date, dtype='datetime64[D]')
    drange = np.append(drange, np.array(end_date, dtype='datetime64[D]'))
    yearfrac = partial(np.vectorize(func),
                       start_date=start_date.astype(dt.datetime),
                       date_format=None,
                       daycount='act/365'
                       )
    #print(yearfrac.keywords)
    tenors = yearfrac(drange.astype(dt.datetime))
    return drange, tenors


#Geometric Brownian motion
def simulate_gbm(x0, start_date, end_date, params, nsims, plot=True):
    drange, times = prepare_tenors(start_date, end_date)
    nperiods = len(times)
    mu = params['mu']
    sigma = params['sigma']
    x = np.zeros((nperiods, nsims), float)
    x[0, :] = x0
    if plot:
        fig_gbm = plt.figure()
    for j in tqdm(range(nsims)):
        z = np.random.standard_normal(nperiods + 1)
        for i in range(1, nperiods):
            x[i, j] = x[i - 1, j] + \
                      mu * x[i - 1, j] * (times[i] - times[i - 1]) + \
                      sigma * x[i - 1, j] * z[i - 1] * np.sqrt(times[i] - times[i - 1])
        if plot and (j % 100) == 0:
            plt.plot(drange.astype(dt.datetime), x[:, j], lw=1)
    if plot:
        plt.grid(True)
        fig_gbm.autofmt_xdate()
        plt.title('Stock price evolution')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
    return x


par_gbm = {'mu':0.1, 'sigma':0.2}
start_date = np.datetime64('2019-05-27')
end_date = np.datetime64('2022-05-27')
x_mat = simulate_gbm(100, start_date, end_date, par_gbm, 10000)


#Orstein-Uhlenbeck process
def simulate_ou(r0, start_date, end_date, params, nsims, plot=True):
    drange, times = prepare_tenors(start_date, end_date)
    nperiods = len(times)
    mu = params['mu']
    sigma = params['sigma']
    alpha = params['alpha']
    r = np.zeros((nperiods, nsims), float)
    r[0, :] = r0
    if plot:
        fig_ou = plt.figure()
    for j in tqdm(range(nsims)):
        z = np.random.standard_normal(len(drange) + 1)
        for i in range(1, len(drange)):
            r[i, j] = r[i - 1, j] + \
                      alpha * (mu - r[i - 1, j]) * (times[i] - times[i - 1]) + \
                      sigma * z[i - 1] * np.sqrt(times[i] - times[i - 1])
        if plot and (j % 100) == 0:
            plt.plot(drange.astype(dt.datetime), r[:, j], lw=1)
    if plot:
        plt.grid(True)
        fig_ou.autofmt_xdate()
        plt.title('Short rate evolution')
        plt.xlabel('Date')
        plt.ylabel('Rate')
        plt.show()
    return r


par_ou = {'mu':0.1, 'sigma':0.2, 'alpha':0.3}
r_mat = simulate_ou(0.095, start_date, end_date, par_ou, 10000)

