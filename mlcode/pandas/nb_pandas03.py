# %%
import pandas as pd
import numpy as np
np.random.seed(6)
np.__version__, pd.__version__

# %%
# Hierarchical Indexing
# Pandas MultiIndex
index = [('California', 2000), ('California', 2010),
         ('New York', 2000), ('New York', 2010),
         ('Texas', 2000), ('Texas', 2010)]
populations = [33871648, 37253956,
               18976457, 19378102,
               20851820, 25145561]
index = pd.MultiIndex.from_tuples(index)
index

# %%
pop = pd.Series(populations, index=index)
pop

# %%
pop[:, 2010]

# %%
# MultiIndex as extra dimension
pop_df = pop.unstack()
pop_df

# %%
pop_df.stack()

# %%
pop_df = pd.DataFrame({'total': pop,
                       'under18': [9267089, 9284094,
                                   4687374, 4318033,
                                   5906301, 6879014]})
pop_df

# %%
f_u18 = pop_df['under18'] / pop_df['total']
f_u18.unstack()


# %%
# Methods of MultiIndex Creation
df = pd.DataFrame(np.random.rand(4, 2),
                  index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns=['data1', 'data2'])
df

# %%
data = {('California', 2000): 33871648,
        ('California', 2010): 37253956,
        ('Texas', 2000): 20851820,
        ('Texas', 2010): 25145561,
        ('New York', 2000): 18976457,
        ('New York', 2010): 19378102}
pd.Series(data)

# %%
# MultiIndex level names
pop.index.names = ['state', 'year']
pop

# %%
# MultiIndex for columns
index = pd.MultiIndex.from_product(
    [[2013, 2014], [1, 2]], names=['year', 'visit'])
columns = pd.MultiIndex.from_product(
    [['Bob', 'Guido', 'Sue'], ['HR', 'Temp']], names=['subject', 'type'])

data = np.round(np.random.randn(4, 6), 1)
data[:, ::2] *= 10
data += 37

health_data = pd.DataFrame(data, index=index, columns=columns)
health_data

# %%
health_data['Guido']


# %%
# Multiply indexed Series
pop

# %%
pop['California', 2000]

# %%
pop['California']

# %%
pop.loc['California':'New York']

# %%
pop[:, 2000]

# %%
cond = pop > 22000000
pop[cond]

# %%
pop[['California', 'Texas']]

# %%
# Multiply indexed DataFrames
health_data

# %%
health_data['Guido', 'HR']

# %%
health_data.iloc[:2, :2]

# %%
health_data.loc[:, ('Bob', 'HR')]

# %%
idx = pd.IndexSlice
health_data.loc[idx[:, 1], idx[:, 'HR']]


# %%
# Sorted and unsorted indices
index = pd.MultiIndex.from_product([['a', 'c', 'b'], [1, 2]])
data = pd.Series(np.random.rand(6), index=index)
data.index.names = ['char', 'int']
data

# %%
try:
    data['a':'b']
except KeyError as e:
    print(type(e))
    print(e)

# %%
data = data.sort_index()
data

# %%
data['a':'b']

# %%
# Stacking and unstacking indices
pop

# %%
pop.unstack(level=0)

# %%
pop.unstack(level=1)

# %%
# Index setting and resetting
pop_flat = pop.reset_index(name='population')
pop_flat

# %%
pop_flat.set_index(['state', 'year'])

# %%
# Data Aggregations on Multi-Indices
health_data

# %%
data_mean = health_data.mean(level='year')
data_mean

# %%
data_mean.mean(axis=1, level='type')


# %%
# Combining Datasets: Concat and Append
def make_df(cols, ind):
    '''Quickly make a DataFrame'''
    data = {c: [str(c) + str(i) for i in ind] for c in cols}
    return pd.DataFrame(data, ind)

# %%
make_df('ABC', range(3))

# %%
class display(object):
    '''Display HTML representation of multiple objects'''
    template = '''<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>'''

    def __init__(self, *args):
        self.args = args

    def _repr_html_(self):
        return '\n'.join(self.template.format(a, eval(a)._repr_html_())
                         for a in self.args)

    def __repr__(self):
        return '\n\n'.join(a + '\n' + repr(eval(a))
                           for a in self.args)
# end display

# %%
# Concatenation of NumPy Arrays
x = [1, 2, 3]
y = [4, 5, 6]
z = [7, 8, 9]
np.concatenate([x, y, z])

# %%
x = [[1, 2], [3, 4]]
np.concatenate([x, x], axis=0)

# %%
np.concatenate([x, x], axis=1)

# %%
# Simple Concatenation with pd.concat
ser1 = pd.Series(['A', 'B', 'C'], index=[1, 2, 3])
ser2 = pd.Series(['D', 'E', 'F'], index=[4, 5, 6])
pd.concat([ser1, ser2])

# %%
df1 = make_df('AB', [1, 2])
df2 = make_df('AB', [3, 4])
display('df1', 'df2', 'pd.concat([df1, df2])')

# %%
df3 = make_df('AB', [0, 1])
df4 = make_df('CD', [0, 1])
display('df3', 'df4', "pd.concat([df3, df4], axis='columns')")

# %%
# The append() method
display('df1', 'df2', 'df1.append(df2)')


# %%
# Duplicate indices
x = make_df('AB', [0, 1])
y = make_df('AB', [2, 3])
y.index = x.index
display('x', 'y', 'pd.concat([x, y])')

# %%
# Catching the repeats as an error
try:
    pd.concat([x, y], verify_integrity=True)
except ValueError as e:
    print('ValueError:', e)

# %%
# Ignoring the index
display('x', 'y', 'pd.concat([x, y], ignore_index=True)')

# %%
# Adding MultiIndex keys
display('x', 'y', "pd.concat([x, y], keys=['x', 'y'])")

# %%
# Concatenation with joins
df5 = make_df('ABC', [1, 2])
df6 = make_df('BCD', [3, 4])
display('df5', 'df6', 'pd.concat([df5, df6])')

# %%
display('df5', 'df6', "pd.concat([df5, df6], join='inner')")

# %%
display('df5', 'df6', 'pd.concat([df5, df6], join_axes=[df5.columns])')

# %%
print('pandas demo done')
