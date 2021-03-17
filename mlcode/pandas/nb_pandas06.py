# %%
import numpy as np
import pandas as pd
np.__version__, pd.__version__

# %%
# Vectorized String Operations
x = np.array([2, 3, 5, 7, 11, 13])
x * 2

# %%
data = ['peter', 'Paul', 'MARY', 'gUIDO']
[s.capitalize() for s in data]

# %%
data = ['peter', 'Paul', None, 'MARY', 'gUIDO']
names = pd.Series(data)
names

# %%
names.str.capitalize()

# %%
# Pandas String Methods
monte = pd.Series(['Graham Chapman', 'John Cleese', 'Terry Gilliam',
                   'Eric Idle', 'Terry Jones', 'Michael Palin'])
monte.str.lower()

# %%
monte.str.len()

# %%
monte.str.startswith('T')

# %%
monte.str.split()

# %%
# Methods using regular expressions
monte.str.extract('([A-Za-z]+)', expand=False)

# %%
# Miscellaneous methods
# Vectorized item access and slicing
monte.str[:3]

# %%
monte.str.split().str.get(-1)

# %%
# Indicator variables
full_monte = pd.DataFrame({'name': monte,
                           'info': ['B|C|D', 'B|D', 'A|C',
                                    'B|D', 'B|C', 'B|C|D']})
full_monte

# %%
full_monte['name'].str.upper()

# %%
full_monte['info'].str.get_dummies('|')


# %%
# pandas.eval() for Efficient Operations
nrows, ncols = 100000, 100
rng = np.random.RandomState(42)
df1, df2, df3, df4 = (pd.DataFrame(rng.rand(nrows, ncols))
                      for i in range(4))

# %%
%timeit df1 + df2 + df3 + df4

# %%
%timeit pd.eval('df1 + df2 + df3 + df4')

# %%
np.allclose(df1 + df2 + df3 + df4,
            pd.eval('df1 + df2 + df3 + df4'))

# %%
# Operations supported by pd.eval()
df1, df2, df3, df4, df5 = (pd.DataFrame(rng.randint(0, 1000, (100, 3)))
                           for i in range(5))
# Arithmetic operators
result1 = -df1 * df2 / (df3 + df4) - df5
result2 = pd.eval('-df1 * df2 / (df3 + df4) - df5')
np.allclose(result1, result2)

# %%
# Comparison operators
result1 = (df1 < df2) & (df2 <= df3) & (df3 != df4)
result2 = pd.eval('df1 < df2 <= df3 != df4')
np.allclose(result1, result2)

# %%
# Bitwise operators
result1 = (df1 < 0.5) & (df2 < 0.5) | (df3 < df4)
result2 = pd.eval('(df1 < 0.5) & (df2 < 0.5) | (df3 < df4)')
np.allclose(result1, result2)

# %%
result3 = pd.eval('(df1 < 0.5) and (df2 < 0.5) or (df3 < df4)')
np.allclose(result1, result3)

# %%
# Object attributes and indices
result1 = df2.T[0] + df3.iloc[1]
result2 = pd.eval('df2.T[0] + df3.iloc[1]')
np.allclose(result1, result2)

# %%
# DataFrame.eval() for Column-Wise Operations
df = pd.DataFrame(rng.rand(1000, 3), columns=['A', 'B', 'C'])
df.head()

# %%
result1 = (df['A'] + df['B']) / (df['C'] - 1)
result2 = pd.eval("(df.A + df.B) / (df.C - 1)")
np.allclose(result1, result2)

# %%
result3 = df.eval('(A + B) / (C - 1)')
np.allclose(result1, result3)

# %%
# Assignment in DataFrame.eval()
df.head()

# %%
df.eval('D = (A + B) / C', inplace=True)
df.head()

# %%
# Local variables in DataFrame.eval()
column_mean = df.mean(1)
column_mean.head()

# %%
result1 = df['A'] + column_mean
result2 = df.eval('A + @column_mean')
np.allclose(result1, result2)

# %%
# DataFrame.query() Method
result1 = df[(df.A < 0.5) & (df.B < 0.5)]
result2 = pd.eval('df[(df.A < 0.5) & (df.B < 0.5)]')
np.allclose(result1, result2)

# %%
result3 = df.query('A < 0.5 and B < 0.5')
np.allclose(result1, result3)

# %%
Cmean = df['C'].mean()
result1 = df[(df.A < Cmean) & (df.B < Cmean)]
result2 = df.query('A < @Cmean and B < @Cmean')
np.allclose(result1, result2)


# %%
# 补充
df = pd.DataFrame(np.arange(6).reshape(2, 3))
df

# %%
df.sum(axis=0)

# %%
df.sum(1)

# %%
df.mean(1)

# %%
# The benefit of eval/query is mainly in the saved memory,
# and the sometimes cleaner syntax they offer.
print('pandas demo done')
