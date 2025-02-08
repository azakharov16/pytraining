### Warm-up ###
import os
import numpy as np
# Yet another difference between sum() and np.sum()
print(sum(0))  # error
print(np.sum(0))

# Python has emoji icons
# Just run 'pip install emoji' in your Terminal
import emoji
print(emoji.emojize(":thumbs_up:"))

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as ss
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

path = 'C://Users//Andrey.Zakharov//PycharmProjects//training//class7'

### 3D Plotting with matplotlib ###
fig = plt.figure()
ax = Axes3D(fig)

# Load volatility data
filename = 'vol_surface.xlsx'
sheetname = 'volatility'
vol = pd.read_excel(path + '//' + filename, sheetname)
strikes = np.arange(50, 160, 10)
tenors = np.array(vol['Yearfrac'])
X, Y = np.meshgrid(tenors, strikes)
Z = np.array(vol.drop(['Tenor', 'Yearfrac'], axis=1)).transpose()

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# The cmap parameter regulates the color map of the surface

# Customize the z-axis
# ax.set_zlim(0.0, 50.0)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

### Simulating an empirical distribution ###

filename = 'stock_data.xlsx'
sheetname = 'OHLC_BA_VOL'
data = pd.read_excel(path + '//' + filename, sheetname, index_col='Date')
data.sort_index(ascending=True, inplace=True)
data['Log_ret'] = np.log(data['Close'] / data['Close'].shift(1))
data['Log_ret'].plot('hist', bins=50)

emp_returns = np.array(data['Log_ret'].dropna(axis=0))
sample_pdf = ss.gaussian_kde(emp_returns)  # Kernel density estimation
sim_returns = sample_pdf.resample(emp_returns.shape[0]).T[:, 0]

# Histogram of initial empirical sample
counts, bins, patches = plt.hist(emp_returns, histtype='step', label='original sample', bins=100,
                                 linewidth=1.5, density=True)
# - counts: the values of histogram bins
# - bins: edges of bins
# - patches: technical list (not used)

# Histogram of datapoints sampled from KDE
plt.hist(sim_returns, histtype='step', label='sample from KDE', bins=bins, linewidth=1.5, density=True)

# The 'histtype' parameter controls the type of histogram
# - 'bar' is a traditional bar-type histogram (if multiple data are given the bars are arranged side by side)
# - 'barstacked' is a bar-type histogram where multiple data are stacked on top of each other
# - 'step' generates a lineplot that is by default unfilled
# - 'stepfilled' generates a lineplot that is by default filled
# The default value is 'bar'

y_kde = sample_pdf(bins)
plt.plot(bins, y_kde, label='KDE')  # visualizing the kernel density function itself
plt.legend()
plt.show()

### Manipulating data frames - a case study ###
import seaborn as sns
df = pd.read_csv(path + '//dataset_collection_proc.csv', header=0, sep=',', encoding='ANSI',
                 low_memory=False)
print(df.shape)
# Dataset description
# - ID_DEBT: identifier of loan contract
# - Bank (hashed): the bank the collection agency has bought a particular portfolio from
# - Portfolio (hashed): a group of overdue contracts from the same bank
# - DPD: days past due
# - DSD: days from the issue date to the date of first delinquency
# - Pension_status: whether the borrower is pensioner
# - Age: age of borrower
# - Uncollectible: some debts are marked by banks as uncollectible
# - Legal: some debts are marked by banks as having the necessary documents for prosecution in court
# - Death: flag of borrower's death
# - Date_cess: date of portfolio purchase
# - Date_sign: date of credit issue
# - Date_birth: borrower's DoB
# - Date_overdue: date of first delinquency
# - Last_pmt_date: date of last payment
# - Loan_amt: amount of credit issued
# - Total_debt: total amount overdue
# - Principal_debt: principal overdue
# - Interest_debt: interest overdue
# - Total_to_loan: ratio of debt to loan amount
# - Principal_to_total: ratio of principal overdue to total debt overdue
# - Sex: borrower's gender
# - Contract_rate: interest rate of credit
# - Paid_amt: how much debt did the borrower repay
# - Last_pmt_sum: sum of last payment before delinquency
# - Region: borrower's region of residence
# - Product: type of credit

# All banks provide data in different formats, so there are a lot of missing values

# Set options for table display
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
# Information about columns and dtypes
print(df.info())
# dtype 'object' indicates either string data or a column with mixed data types
# Note that df.info() is helpful when detecting missing data
types = df.dtypes
# Set options for float numbers display (only 2 digits after .)
pd.options.display.float_format = '{:,.2f}'.format
df.describe(include=['int64', 'float64'])

# Drop duplicated and missing IDs
primary_key = 'ID_DEBT'
if df[primary_key].nunique() != df.shape[0]:
    df.drop_duplicates(subset=primary_key, keep='first', inplace=True)
    df.dropna(subset=primary_key, axis=0, inplace=True)
    df[primary_key] = df[primary_key].astype('int')
# Other options for .drop_duplicates() function are 'last' and 'none'

# Set index
df.set_index(primary_key, inplace=True, drop=True)

# Check the dataset for empty rows
if df[df.isna().all(axis=1)].shape[0] != 0:
    df = df[df.notna().any(axis=1)]

# Convert and refine categorical columns
# Refine gender column
counts = df['Sex'].value_counts()  # view counts of each unique value
df = df[~df['Sex'].isin(['ИП', 'ЮЛ', 'ОАО', 'ООО'])]
gender_dict = {'FEMALE':'F','MALE':'M','Female':'F','Male':'M', 'Женский':'F', 'Мужской':'M',
               'М':'M', 'Ж':'F', 'м':'M', 'ж':'F'}
df['Sex'] = df['Sex'].map(lambda x: gender_dict.get(str(x).strip(), 'U'))
df['Sex'].value_counts(normalize=True)  # view proportion of each unique value
# Refine region column
region_tab = pd.read_csv(path + '//region_mapping.csv', header=0, sep=',', encoding='ANSI')
region_tab.rename(columns={'Наименование_старое':'Region_old', 'Наименование':'Region_new'},
                  inplace=True)
s = df.shape[0]
df = pd.merge(df, region_tab, left_on='Region', right_on='Region_old', how='left')
assert df.shape[0] == s
df.drop(['Region', 'Region_old'], axis=1, inplace=True)
# Refine product column
product_tab = pd.read_csv(path + '//product_mapping.csv', header=0, sep=';', encoding='ANSI')
df = pd.merge(df, product_tab, left_on='Product', right_on='PRODUCT_MY', how='left')
assert df.shape[0] == s
df.drop(['Product', 'PRODUCT_MY'], axis=1, inplace=True)
df.rename(columns={'Region_new':'Region', 'PRODUCT_MY_calc':'Product'}, inplace=True)

# Process the pension flag and age column
print(df['Pension_status'].unique().tolist())
df = df[df['Pension_status'] != 'ЮР/МСБ']
pens_dict = {'NOT_PENSIONER':0, 'PENSIONER':1}
df['Pension_status'] = df['Pension_status'].map(lambda x: pens_dict.get(x, np.nan))
print(df['Pension_status'].isna().sum())
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Age'].describe()
df = df[df['Age'] >= 18]
df['Age'] = df['Age'].fillna(np.round(df['Age'].mean())).astype('int')
df[(df['Sex'] == 'M') & df['Age'] > 60]['Pension_status'] = 1
df[(df['Sex'] == 'F') & df['Age'] > 55]['Pension_status'] = 1
df['Pension_status'] = df['Pension_status'].fillna(0).astype('int')
# Processing the uncollectible flag
print(df['Uncollectible'].unique().tolist())
df['Uncollectible'] = df['Uncollectible'].replace(np.nan, 0).astype('int')
# Processing the death flag
print(df['Death'].unique().tolist())
df['Death'] = df['Death'].replace('Y ', 1)
df['Death'] = pd.to_numeric(df['Death'], errors='coerce')
df['Death'] = df['Death'].replace(np.nan, 0).astype('int')
# Processing the legal flag
print(df['Legal'].unique().tolist())
df['Legal'] = df['Legal'].replace(np.nan, 0).astype('int')
# Rename flag columns
df.rename(columns={'Uncollectible':'Uncollect_flag', 'Pension_status':'Pensioner_flag',
                   'Death':'Death_flag', 'Legal':'Legal_flag'}, inplace=True)

# Processing last payment period
counts = df['Last_pmt_period'].value_counts()
df['Last_pmt_period'] = df['Last_pmt_period'].replace('NO_PAYMENTS', '360+')
bucket_dict = {'0-30': 1, '30-60': 2, '60-90': 3, '90-180': 4, '180-360': 5, '360+': 6}
df['Bucket'] = df['Last_pmt_period'].map(lambda x: bucket_dict.get(x, np.nan))
bucket_bins = np.array([0, 30, 60, 90, 180, 360], int)
df['Last_pmt_period'] = pd.to_numeric(df['Last_pmt_period'], errors='coerce')
df.where(df['Bucket'].isna())['Bucket'] = np.digitize(
    df.where(
        (~df['Last_pmt_period'].isin(bucket_dict.keys())) & (
         df['Last_pmt_period'].notna())
    )['Last_pmt_period'], bucket_bins)
df.drop('Last_pmt_period', axis=1, inplace=True)
print(df['Bucket'].isna().sum())
df['Bucket'] = df['Bucket'].replace(np.nan, -999999).astype('int')

# Select columns based on regular expression
date_cols = df.filter(regex='^Date_').columns.values.tolist() + ['Last_pmt_date']
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')
flag_cols = df.filter(regex='_flag$').columns.values.tolist()
cat_cols = ['Product', 'Region', 'Bank', 'Bucket', 'Portfolio']

# Processing numeric columns
# Use existing column sets to identify numeric columns
num_cols = [col for col in df.columns.values if col not in date_cols + flag_cols + cat_cols]
num_cols.remove('Age')
num_cols.remove('Sex')

# Processing DPD and DSD
df['DPD'] = pd.to_numeric(df['DPD'], errors='coerce')
df['DSD'] = pd.to_numeric(df['DSD'], errors='coerce')
df[['DPD', 'DSD']].describe()
df.loc[df['DPD'] < 0, 'DPD'] = np.nan
df['DPD'] = df['DPD'].fillna(-1).astype('int')
num_cols.remove('DPD')
df.loc[df['DSD'] < 0, 'DSD'] = np.nan
df['DSD'] = df['DSD'].fillna(-1).astype('int')
num_cols.remove('DSD')
df.loc[df['Total_debt'] > df['Loan_amt'], 'Total_debt'] = df['Loan_amt']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    q_up = df[col].quantile(0.95)
    df[col] = df[col].clip(lower=0, upper=q_up)
    df_grouped = df.groupby('Portfolio')[col].mean()
    df.loc[df[col].isna(), col] = df['Portfolio'].map(df_grouped)

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())

df['Total_to_loan'] = df['Total_debt'] / df['Loan_amt']
# Using encoding for categorical columns
# One-hot encoding
df = pd.get_dummies(df, columns=['Sex'])

# Generate target variable
df['Response'] = np.random.choice([0, 1], size=df.shape[0], p=[0.9, 0.1]).astype('int')
df['Response'].value_counts()
df['Response'].value_counts(normalize=True)

# Summary statistics on portfolio level
target_avg = df.groupby('Portfolio')['Response'].mean()
dpd_dsd_stats = df.groupby('Portfolio', as_index=False)[['DPD','DSD']].agg(['max', 'sum', 'mean'])
target_dpd_stats = df.groupby('Portfolio', as_index=False).agg({'DPD':['max', 'sum'], 'Response':'mean'})
print(type(target_dpd_stats.columns))
print(target_dpd_stats.columns.values)
target_dpd_stats.sort_values(('Response', 'mean'), ascending=False, inplace=True)
summary_tab1 = pd.crosstab(df['Portfolio'], df['Response'], normalize=False)
summary_tab2 = pd.crosstab(df['Portfolio'], df['Response'], normalize=True)
print(summary_tab2.sum(axis=0))
pivot_tab_port = df.pivot_table(values=['Response', 'Total_debt'], index=['Portfolio'], aggfunc='mean')
pivot_tab_buck = df.pivot_table(values=['Response', 'Total_debt'], index=['Bucket'], aggfunc='median')

# Mean encoding
cat_cols.remove('Portfolio')
glob_mean = df['Response'].mean()
for col in cat_cols:
    mean_series = df.groupby(col)['Response'].mean()
    df[col + '_enc'] = df[col].map(mean_series)
    df[col + '_enc'] = df[col + '_enc'].fillna(glob_mean)

# Alternative way: define categorical variables explicitly and pass them into ML model
# Method 1:
for col in cat_cols:
    df[col] = df[col].astype('category')
# Method 2:
product_cats = pd.Categorical(df['Product'].tolist(), categories=['POTREB', 'CARDS', 'AVTO'],
                              ordered=False)
df['Product_cat'] = pd.Series(product_cats)
print(df['Product_cat'].unique().tolist())
df.drop(cat_cols + ['Product_cat'], axis=1, inplace=True)

### Visual analysis ###
df.plot.scatter(x='DPD', y='DSD')
df.groupby('Portfolio')['Total_debt', 'Principal_debt', 'Interest_debt'].mean().plot(kind='bar', rot=45)

# Correlation matrix
sns.heatmap(df[num_cols].corr(method='spearman'))  # note that missing values are not allowed
# Histogram
df['Total_to_loan'] = df['Total_to_loan'].fillna(0.0)
sns.set()
sns.distplot(df['Total_to_loan'])
# Combining scatter plots and histograms
sns.jointplot(df['Loan_amt'], df['Total_debt'])
sns.pairplot(df[['Total_debt', 'Principal_debt', 'Interest_debt']])
# Basic box plot
sns.boxplot(df['Loan_amt'], orient='v')
# Box plot by category
sns.boxplot(y='Pensioner_flag', x='Loan_amt', data=df, orient='h')
# Basic countplot
sns.countplot(x='Legal_flag', hue='Bucket', data=df)

sns.violinplot(x='Legal_flag', y='Total_debt', data=df)

# Save the refined dataset
os.chdir(path)
df.to_csv('dataset_collection_refined.csv', sep=',', header=True, index=True, encoding='ANSI')
