# %%
import numpy as np
import pandas as pd
np.__version__, pd.__version__

# Working with Time Series
# Native Python dates and times: datetime and dateutil
from datetime import datetime
datetime(year=2015, month=7, day=4)

# %%
from dateutil import parser
date = parser.parse('4th of July, 2015')
date

# %%
date.strftime('%A')

# %%
# Typed arrays of times: NumPy's datetime64
date = np.array('2015-07-04', dtype=np.datetime64)
date

# %%
date + np.arange(12)

# %%
np.datetime64('2015-07-04')

# %%
np.datetime64('2015-07-04 12:00')

# %%
np.datetime64('2015-07-04 12:59:59.50', 'ns')

# %%
# Dates and times in pandas
date = pd.to_datetime('4th of July, 2015')
date

# %%
date.strftime('%A')

# %%
date + pd.to_timedelta(np.arange(12), 'D')


# %%
# Pandas Time Series: Indexing by Time
index = pd.DatetimeIndex(['2014-07-04', '2014-08-04',
                          '2015-07-04', '2015-08-04'])
data = pd.Series([0, 1, 2, 3], index=index)
data

# %%
data['2014-07-04':'2015-07-04']

# %%
data['2015']

# %%
# Pandas Time Series Data Structures
dates = pd.to_datetime([datetime(2015, 7, 3), '4th of July, 2015',
                        '2015-Jul-6', '07-07-2015', '20150708'])
dates

# %%
dates.to_period('D')

# %%
dates - dates[0]

# %%
# Regular sequences: pd.date_range()
pd.date_range('2015-07-03', '2015-07-10')

# %%
pd.date_range('2015-07-03', periods=8)

# %%
pd.date_range('2015-07-03', periods=8, freq='H')

# %%
pd.period_range('2015-07', periods=8, freq='M')

# %%
pd.timedelta_range(0, periods=10, freq='H')


# %%
# Example: Visualizing Seattle Bicycle Counts
data = pd.read_csv('data/FremontBridge.csv',
                   index_col='Date', parse_dates=True)
data.head()

# %%
data.columns = ['Total', 'West', 'East']
# data['Total'] = data.eval('West + East')
data.head()

# %%
data.dropna().describe()

# %%
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn

seaborn.set()
data.plot()
# x轴为index(date), y轴为col值
plt.ylabel('Hourly Bicycle Count')

# %%
weekly = data.resample('W').sum()
weekly.plot(style=[':', '--', '-'])
plt.ylabel('Weekly bicycle count')

# %%
daily = data.resample('D').sum()
daily.rolling(30, center=True).sum().plot(style=[':', '--', '-'])
plt.ylabel('Mean hourly count')

# %%
# Digging into the data
by_time = data.groupby(data.index.time).mean()
hourly_ticks = 4 * 60 * 60 * np.arange(6)
by_time.plot(xticks=hourly_ticks, style=[':', '--', '-'])

# %%
by_weekday = data.groupby(data.index.dayofweek).mean()
by_weekday.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
by_weekday

# %%
by_weekday.plot(style=[':', '--', '-'])

# %%
weekend = np.where(data.index.weekday < 5, 'Weekday', 'Weekend')
by_time = data.groupby([weekend, data.index.time]).mean()
by_time.head()

# %%
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
by_time.ix['Weekday'].plot(ax=ax[0], title='Weekdays',
                           xticks=hourly_ticks, style=[':', '--', '-'])
by_time.ix['Weekend'].plot(ax=ax[1], title='Weekends',
                           xticks=hourly_ticks, style=[':', '--', '-'])

# %%
print('pandas demo done')
