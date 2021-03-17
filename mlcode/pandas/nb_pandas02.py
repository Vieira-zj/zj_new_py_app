# %%
# Operating on Data in Pandas
import pandas as pd
import numpy as np
np.random.seed(6)
np.__version__, pd.__version__

# %%
# Ufuncs: Index Preservation
rnd = np.random.RandomState(42)
ser = pd.Series(rnd.randint(0, 10, 4))
ser

# %%
np.exp(ser)

# %%
df = pd.DataFrame(rnd.randint(0, 10, (3, 4)), columns=['A', 'B', 'C', 'D'])
df

# %%
np.sin(df * np.pi / 4)


# %%
# Index alignment in Series
area = pd.Series({'Alaska': 1723337, 'Texas': 695662,
                  'California': 423967}, name='area')
population = pd.Series({'California': 38332521, 'Texas': 26448193,
                        'New York': 19651127}, name='population')
population / area

# %%
# union
area.index | population.index

# %%
A = pd.Series([2, 4, 6], index=[0, 1, 2])
B = pd.Series([1, 3, 5], index=[1, 2, 3])
A + B

# %%
A.add(B, fill_value=0)

# %%
# Index alignment in DataFrame
A = pd.DataFrame(rnd.randint(0, 20, (2, 2)), columns=list('AB'))
A

# %%
B = pd.DataFrame(rnd.randint(0, 10, (3, 3)), columns=list('BAC'))
B

# %%
A + B

# %%
fill = A.stack().mean()
A.add(B, fill_value=fill)


# %%
# Operations Between DataFrame and Series
A = rnd.randint(10, size=(3, 4))
A

# %%
A - A[0]

# %%
df = pd.DataFrame(A, columns=list('QRST'))
df

# %%
df - df.iloc[0]

# %%
df.subtract(df['R'], axis=0)


# %%
# Handling Missing Data
# None: Pythonic missing data
vals1 = np.array([1, None, 3, 4])
vals1

# %%
# NaN: Missing numerical data
vals2 = np.array([1, np.nan, 3, 4])
print(vals2.dtype)
vals2

# %%
print(1 + np.nan)
print(0 * np.nan)

# %%
vals2.sum(), vals2.max(), vals2.min()

# %%
np.nansum(vals2), np.nanmin(vals2), np.nanmax(vals2)

# %%
# NaN and None in Pandas
pd.Series([1, np.nan, 2, None])

# %%
# Detecting null values
data = pd.Series([1, np.nan, 'hello', None])
data.isnull()

# %%
cond = data.notnull()
data[cond]


# %%
# Dropping null values
data.dropna()

# %%
df = pd.DataFrame([[1,      np.nan, 2],
                   [2,      3,      5],
                   [np.nan, 4,      6]])
df

# %%
df.dropna()

# %%
df.dropna(axis=1)

# %%
df.dropna(axis='columns')

# %%
df[3] = np.nan
df

# %%
df.dropna(axis='columns', how='all')


# %%
# Filling null values
data = pd.Series([1, np.nan, 2, None, 3], index=list('abcde'))
data

# %%
data.fillna(0)

# %%
data.fillna(method='ffill')  # forward-fill

# %%
data.fillna(method='bfill')  # back-fill

# %%
print('pandas demo done')
