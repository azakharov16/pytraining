from itertools import repeat
import warnings
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot

### Warm-up ###
import statsmodels.api as sm

# Generate artificial data (2 regressors + constant)
nobs = 100
X = np.random.random((nobs, 2))
X = sm.add_constant(X)
beta = [1.0, 0.1, 0.5]
noise = np.random.standard_normal(size=nobs)
y = np.dot(X, beta) + noise

# Fit regression model
results = sm.OLS(y, X).fit()

# Inspect the results
print(results.summary())

### Interactive plots with plotly ###
filename = 'stock_data.xlsx'
sheet = 'OHLC_BA_VOL'
path = 'C://Users//andrey.zakharov//PycharmProjects//training//class8'
df = pd.read_excel(path + '//' + filename, sheet)
df.set_index('Date', inplace=True, drop=True)
df['Logret'] = np.log(df['Close'] / df['Close'].shift(1))
col_list = df.columns.drop(['Logret', 'Volume']).values.tolist()
agg_dict = dict(zip(col_list, repeat(np.mean, len(col_list))))
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    df_mon = df.resample('M').agg({
        'Logret':[np.nanmean, np.nanstd], 'Volume':np.nansum, **agg_dict
    })

# Line chart
trace0 = go.Scatter(x=df_mon.index, y=df_mon[('Logret', 'nanmean')], name='Mean return')
trace1 = go.Scatter(x=df_mon.index, y=df_mon[('Logret', 'nanstd')], name='Return std')
data = [trace0, trace1]
layout = {'title': 'Statistics of trading activity'}
fig = go.Figure(data=data, layout=layout)
iplot(fig, show_link=False)
plotly.offline.plot(fig, filename='trading_stats.html', show_link=False)

# Bar chart
trace0 = go.Bar(x=df_mon.index, y=df_mon[('High', 'mean')], name='High')
trace1 = go.Bar(x=df_mon.index, y=df_mon[('Low', 'mean')], name='Low')
data = [trace0, trace1]
layout = {'title': 'High and low averages', 'xaxis': {'title': 'Period'}}
fig = go.Figure(data=data, layout=layout)
iplot(fig, show_link=False)
plotly.offline.plot(fig, filename='high_low.html', show_link=False)

# Scatter plot
trace0 = go.Scatter(mode='markers', x=df_mon[('Ask', 'mean')], y=df_mon[('Bid', 'mean')], name='Bid-ask spread')
data = [trace0]
layout = {'title': 'Avegare bid-ask spread analysis'}
fig = go.Figure(data=data, layout=layout)
iplot(fig, show_link=False)
plotly.offline.plot(fig, filename='bid_ask_scatter.html', show_link=False)

# 3D scatter plot
trace0 = go.Scatter3d(
    mode='markers',
    x=df['Ask'],
    y=df['Bid'],
    z=df.index,
    name='Bid-ask spread'
)
data = [trace0]
layout = {'title': 'Bid-ask spread analysis'}
fig = go.Figure(data=data, layout=layout)
iplot(fig, show_link=False)
plotly.offline.plot(fig, filename='bid_ask_scatter3d.html', show_link=False)

# Box plot
data = []
for y in df.index.year.unique():
    data.append(
        go.Box(y=df[df.index.year==y]['Logret'], name=y)
    )
layout = {'title': 'Log returns by year', 'xaxis': {'title': 'year'}, 'yaxis': {'title': 'logreturn'}}
fig = go.Figure(data=data, layout=layout)
iplot(fig, show_link=False)
plotly.offline.plot(fig, filename='returns_boxplots.html', show_link=False)

# Calling plotly directly on a dataframe with cufflinks
# NOTE that such integration works in either PyCharm Professional edition or Jupyter Notebook
import cufflinks as cf
cf.go_offline()
df['Close'].iplot(kind='line', xTitle='Date', yTitle='Close price', title='Stock price dynamics', filename = 'price_chart.html')
df[['Open', 'Close', 'High', 'Low']].scatter_matrix(filename='prices_scatter', world_readable=False)
