import numpy as np
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt

### Pandas built-in routines for type conversions in ndarrays, series or dataframes ###
foo1 = np.array(['2019-05-16', '2-0-1-9'], dtype=str)
foo2 = np.array(['1', '2.1', '3,1'], dtype=str)
foo_nums = pd.to_numeric(foo2, errors='coerce')
print(foo_nums)
foo_dates = pd.to_datetime(foo1, errors='coerce')
print(foo_dates)
# Dealing with wrong data formats in type conversion:
# - errors='raise': if any data in the wrong format is present, a ValueError will be raised
# - errors='ignore': any data in the wrong format will be left unchanged
# - errors='coerce': any data in the wrong format will be replaced with np.nan or pd.NaT
print(np.isnat(foo_dates))  # works only on ndarrays of datetime data type
del foo1, foo2, foo_nums, foo_dates
# Numpy has the .astype() equivalent, but it does not support safe type conversions

print(bool(np.nan))
print(bool(pd.NaT))
print(np.nan + pd.NaT)
print(np.nan - pd.NaT)
print(pd.NaT + np.nan)
print(pd.NaT - np.nan)

### Date and Time objects in pandas ###
d = pd.to_datetime('15-05-2019', dayfirst=True)
print(type(d))
ts = pd.Timestamp('2019-05-15')
drange = pd.date_range(ts, periods=500, freq='D')  # generates a pd.DatetimeIndex object

np.random.seed(123456)

# Simulation of Random Walk process
rnd = np.random.standard_normal(size=len(drange)).cumsum()
fig = plt.figure()
plt.plot(drange, rnd)
plt.grid(True)
fig.autofmt_xdate()  # auto-formatting of datetime x-ticks
plt.show()

### Introduction to series ###
s = pd.Series(rnd, index=drange)
print(sum(s.values.tolist()))
print(max(s.index.tolist()))
print(min(s.index.tolist()))
# The pd.Series object has almost all numpy member functions as attributes
print(s.mean())
print(s.sum())

# Rolling computations with series
s_abs = s.map(lambda x: abs(x))
# NOTE: a series is a 1D equivalent of a data frame

### Introduction to Data Frames ###
df = pd.DataFrame({'col1':[1,2,3], 'col2':[4,5,6]}, index=['a', 'b', 'c'])
print(df.index.tolist())
print(df.columns.tolist())
print('a' in df.index)
print('col3' in df.columns)
pprint(df.to_dict())

column_locator = df['col1']  # df.col1
print(type(column_locator))
index_locator = df.loc['a']
print(type(index_locator))
position_locator = df.iloc[2]
print(type(position_locator))
print(df.at['a', 'col2'])

df_new = pd.DataFrame({'col1':[7,8,9], 'col2':[10,11,12]}, index=['d', 'e', 'f'])
df = df.append(df_new)
df = df.apply(lambda x: x ** 2)
df.reset_index(inplace=True, drop=True)
df_long = pd.concat([df, df_new], axis=0, ignore_index=True)
df_new.rename(columns={'col1':'col3', 'col2':'col4'}, inplace=True)
df = df.iloc[0:3]
df_new.reset_index(inplace=True, drop=True)
df = pd.concat([df, df_new], axis=1)

### Example: plotting stock prices ###
path = 'C://Users//andrey.zakharov//PycharmProjects//training//class6'
filename = 'stock_data.xlsx'
sheet1 = 'OHLC_BA_VOL'
stock_data = pd.read_excel(path + '//' + filename, sheet1)
stock_data.head()
stock_data.tail()
stock_data.info()
summary = stock_data.describe()
print(stock_data.dtypes)
stock_data.set_index('Date', inplace=True, drop=True)
# Another method: stock_data.index = pd.DatetimeIndex(stock_data['Date'])
stock_data.drop('Volume', axis=1, inplace=True)
# Another method: del stock_data['Volume']
stock_data.sort_index(ascending=True, inplace=True)
stock_data[['Close', 'High', 'Low']].plot(subplots=True, style=['b', 'g', 'r'], figsize=(10,15))

sheet2 = 'VWAP'
vwap_data = pd.read_excel(path + '//' + filename, sheet2)
vwap_data.set_index('Date', inplace=True, drop=True)

stock_data = pd.merge(stock_data, vwap_data, left_index=True, right_index=True, how='left')
print(stock_data['VWAP'].isna().sum())  # note that .isna() catches both np.nan and pd.NaT
stock_data['VWAP'] = stock_data.fillna(method='bfill')  # index-aware interpolation
stock_data['Avg_vwap_6M'] = stock_data['VWAP'].rolling(window=126, center=False).mean()
stock_data[['VWAP', 'Avg_vwap_6M']].plot(subplots=False, grid=True, lw=1.5, figsize=(10,10))

# Note that .plot() is a wrapper method around matplotlib's plt.plot() function
