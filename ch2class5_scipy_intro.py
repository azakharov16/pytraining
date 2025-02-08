"""
Scipy submodules
> scipy.constants      #Mathematical constants
> scipy.special        #Special functions
> scipy.integrate      #Numeric integration
> scipy.optimize       #General-purpose optimization
> scipy.linalg         #Linear algebra library
> scipy.sparse         #Dealing with large sparse matrices
> scipy.interpolate    #Interpolation
> scipy.fftpack        #Fast Fourier Transformations
> scipy.signal         #Convolution, filtering, correlations
> scipy.stats          #Statistical functions and probability distributions
"""
# NOTE : some scipy submodules require explicit import

import sys
import numpy as np
import scipy as sp
import scipy.stats as ss
import datetime as dt
from matplotlib import pyplot as plt
from functools import partial
from pprint import pprint

path = 'C://Users//andrey.zakharov//PycharmProjects//training//class5'
sys.path.append(path)
from yearfrac import yearfrac

# Simple plotting
def func(x):
    return x * np.sin(x)
x = np.arange(-10, 10, 0.01)
plt.plot(x, func(x))
plt.show()

# Basic optimization
xmin = sp.optimize.fmin_bfgs(func, 0.1)
print(*xmin)
# The optimizer identifies local extrema only. Setting the disp argument to zero suppresses verbose output
xmin = sp.optimize.fmin_bfgs(func, 4, disp=0)
print(*xmin)

# Finding roots
solution = sp.optimize.fsolve(lambda x: x - np.cos(x), x0=np.pi / 2)
print(*solution)

### Interpolation ###

spot_rates = np.array([0.0218088, 0.021825, 0.0221425, 0.0240019, 0.0254525, 0.0277106,
                        0.0288581, 0.0310056, 0.0287091, 0.0283616, 0.028191, 0.0281507,
                        0.0282218, 0.028358, 0.0285521, 0.02877, 0.0290043], dtype = float)
dates = np.array(
            ['12/13/2018', '12/14/2018', '12/19/2018', '1/12/2019', '2/12/2019', '3/12/2019',
             '6/12/2019', '12/12/2019', '12/12/2020', '12/12/2021', '12/12/2022', '12/12/2023',
             '12/12/2024', '12/12/2025', '12/12/2026', '12/12/2027', '12/12/2028'],
             dtype = dt.datetime
             )
valuation_date = dt.date(2018,12,12)
yearfrac = partial(np.vectorize(yearfrac),
                   start_date=valuation_date,
                   date_format='%m/%d/%Y',
                   daycount='30/360'
                   )
tenors = yearfrac(dates)

tenors_seq = np.arange(np.round(np.min(tenors), 4), np.round(np.max(tenors), 4), 0.0001)

maturity_date = dt.date(2020,12,5)
tau = yearfrac(maturity_date)
r = np.interp(tau, tenors, spot_rates)
print(r)
# Note that np.interp() works faster than scipy.interpolate.interp1d(), but supports linear interpolation only

linear_interp = sp.interpolate.interp1d(tenors, spot_rates, kind='linear')
rates_linear = linear_interp(tenors_seq)
plt.plot(tenors, spot_rates, 'o', tenors_seq, rates_linear, '-')
plt.ylim(np.round(np.min(spot_rates), 2) - 0.005, np.round(np.max(spot_rates), 2) + 0.005)
plt.show()

spline_interp = sp.interpolate.interp1d(tenors, spot_rates, kind='cubic')
rates_spline = spline_interp(tenors_seq)
plt.plot(tenors, spot_rates, 'o', tenors_seq, rates_spline, '-')
plt.ylim(np.round(np.min(spot_rates), 2) - 0.005, np.round(np.max(spot_rates), 2) + 0.005)
plt.show()

# Function for fitting the Nelson-Siegel-Svensson model via OLS for some initial guess of lambdas
def fit_nss(spot_rates, tenors, lambda1, lambda2):
    y_vec = np.transpose(spot_rates[np.newaxis, :])
    x1 = (1 - np.exp(-tenors / lambda1)) / (tenors / lambda1)
    x2 = x1 - np.exp(-tenors / lambda1)
    x3 = (1 - np.exp(-tenors / lambda2)) / (tenors / lambda2) - np.exp(-tenors / lambda2)
    x_mat = np.concatenate((np.ones_like(y_vec), x1[:, np.newaxis], x2[:, np.newaxis], x3[:, np.newaxis]), axis=1)
    beta_vec = np.dot(np.dot(np.linalg.inv(np.dot(x_mat.T, x_mat)), x_mat.T), y_vec)
    mse = np.sum((np.dot(x_mat, beta_vec) - y_vec) ** 2)
    return beta_vec, mse

# Function to calculate the predicted values of the NSS model
def nss_interp(tau, beta_vec, lambda1, lambda2):
    x1 = np.transpose((1 - np.exp(-tau / lambda1)) / (tau / lambda1))
    x2 = np.transpose(x1 - np.exp(-tau / lambda1))
    x3 = np.transpose((1 - np.exp(-tau / lambda2)) / (tau / lambda2) - np.exp(-tau / lambda2))
    y = beta_vec[0] + beta_vec[1] * x1 + beta_vec[2] * x2 + beta_vec[3] * x3
    return y

mse_arr = []
l1_arr = []
l2_arr = []
for l1 in np.arange(0.1, 2.0, 0.1):
    for l2 in np.arange(5.0, 20.0, 0.5):
        beta, mse = fit_nss(spot_rates, tenors, lambda1=l1, lambda2=l2)
        mse_arr.append(mse)
        l1_arr.append(l1)
        l2_arr.append(l2)
best_model_num = [num for (num, m) in enumerate(mse_arr) if m == min(mse_arr)].pop(0)
l1_best = l1_arr[best_model_num]
l2_best = l2_arr[best_model_num]
# Fitting the best model with OLS
beta_best, _ = fit_nss(spot_rates, tenors, lambda1=l1_best, lambda2=l2_best)
# Using NSS to interpolate the basis curve
rates_nss = np.array([], float)
for t in tenors_seq:
    rates_nss = np.append(rates_nss, nss_interp(t, beta_best, lambda1=l1_best, lambda2=l2_best))
plt.plot(tenors, spot_rates, 'o', tenors_seq, rates_nss, '-')
plt.ylim(np.round(np.min(spot_rates), 2) - 0.005, np.round(np.max(spot_rates), 2) + 0.005)
plt.show()

### Working with random variables ###
print(ss.norm.ppf(0.95))
x = np.arange(-5, 5, 0.0001)
plt.plot(x, ss.norm.pdf(x))
plt.show()
print(ss.norm.cdf(1.96))

### Numpy random module ###
np.random.seed(123456)
# Generate random numbers inside [0;1)
print(np.random.rand(5))
print(np.random.rand(2, 3))
b = np.random.rand(100).reshape(10, 10)
pprint(np.cov(b))
pprint(np.corrcoef(b))
pprint(ss.spearmanr(b).correlation)
pprint(ss.spearmanr(b).pvalue)

# Generate a single random number inside [0;1)
print(np.random.random())
# Generate random integer inside an interval
print(np.random.randint(5, 10))
# Generate random floats in the half-open interval [0.0, 1.0)
pprint(np.random.sample(size=(5, 10)))
# Draw numbers from other distributions:
print(np.random.poisson(6.0))
print(np.random.normal(1.5, 4.0))
print(np.random.normal())
print(np.random.normal(size=5))
# Other distributions are available: beta, binomial, chisquare, dirichlet, exponential, f,
# gamma, geometric, gumbel, hypergeometric, laplace, logistic, lognormal, multinomial,
# multivariate_normal, negative_binomial, noncentral_chisquare, noncentral_f, pareto,
# rayleigh, standard_cauchy, standard_t, uniform, vonmises, wald, weibull, zipf

# Plotting histograms
h = plt.hist(np.random.normal(size=100000), bins=200, normed=True)
plt.show()

# The np.random.choice(a, size=None, replace=True, p=None) function
# - if a is an ndarray, the sample is generated from its elements
# - if a is an int, the random sample is generated as if a = np.arange(a)
# - size is the output shape (int, tuple or None); if None, a single value is returned
# - p is the probability array associated with a; if None, uniform distribution is assumed
a = np.random.choice(5, size=3, replace=False, p=[0.1, 0.0, 0.3, 0.6, 0.0])
print(a)
