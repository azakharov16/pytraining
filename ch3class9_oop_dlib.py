import numpy as np
import scipy as sp
import scipy.stats as ss
from matplotlib import pyplot as plt

class VanillaOption(object):
    def __init__(self, spot, strike, tenor, vol, rf, option_type):
        self.S = spot
        self.K = strike
        self.T = tenor
        self.sigma = vol
        self.r = rf
        self.option_type = option_type
        if self.option_type not in ('call', 'put'):
            raise ValueError("Error: the option type must be either 'call' or 'put'!")
    def __VanillaPrice(self, S, K, T, sigma, r, option_type):
        def d1(S, K, T, sigma, r):
            return (np.log(S / K) + (r + 0.5 * pow(sigma,2) * T) / (sigma * np.sqrt(T)))
        def d2(S, K, T, sigma, r):
            return (np.log(S / K) + (r - 0.5 * pow(sigma,2) * T) / (sigma * np.sqrt(T)))
        def vanilla_call_price(S, K, T, sigma, r):
            price = S * ss.norm.cdf(d1(S, K, T, sigma, r)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S, K, T, sigma, r))
            return price
        def vanilla_put_price(S, K, T, sigma, r):
            price = -S * ss.norm.cdf(-d1(S, K, T, sigma, r)) + K * np.exp(-r * T) * ss.norm.cdf(-d2(S, K, T, sigma, r))
            return price
        pricefunc = {'call':vanilla_call_price, 'put':vanilla_put_price}[option_type]
        return pricefunc(S, K, T, sigma, r)
    def BlackScholesPrice(self):
        return self.__VanillaPrice(self.S, self.K, self.T, self.sigma, self.r, self.option_type)
    def SetMarketPrice(self, mprice):
        self.mprice = mprice
    def ImpliedVol(self, start_value = 0.1):
        self.sigmastart = start_value
        vimp = sp.optimize.fmin_bfgs(
            lambda x: abs(
                self.__VanillaPrice(self.S, self.K, self.T, x, self.r, self.option_type) - self.mprice
            ), self.sigmastart, disp=0)
        return float(vimp)

c = VanillaOption(95.0, 100.0, 1.15, 0.2, 0.05, 'call')
print(c.BlackScholesPrice())
c.SetMarketPrice(8.5)
print(c.ImpliedVol())

class OptionDelta(object):
    def __init__(self, option):
        self.S = option.S
        self.K = option.K
        self.T = option.T
        self.sigma = option.sigma
        self.r = option.r
        self.option_type = option.option_type
    def __d1(self, spot):
            return (np.log(spot / self.K) + (self.r + 0.5 * pow(self.sigma,2) * self.T) / (self.sigma * np.sqrt(self.T)))
    def CalculateGreek(self, spot):
        def call_delta(d):
            return ss.norm.cdf(d)
        def put_delta(d):
            return (ss.norm.cdf(d) - 1)
        delta_func = {'call':call_delta,'put':put_delta}[self.option_type]
        return delta_func(self.__d1(spot))
    def PlotGreek(self, xlow = 0.01, xhigh = 200):
        spot_range = np.linspace(xlow, xhigh, 1000)
        values = np.vectorize(self.CalculateGreek)(spot_range)
        plt.plot(spot_range, values)
        plt.grid(True)

c_delta = OptionDelta(c)
print(c_delta.CalculateGreek(80))
c_delta.PlotGreek()

p = VanillaOption(90, 100, 1.5, 0.3, 0.05, 'put')
print(p.BlackScholesPrice())
p.SetMarketPrice(13.9)
print(p.ImpliedVol())

p_delta = OptionDelta(p)
print(p_delta.CalculateGreek(80))
p_delta.PlotGreek()

