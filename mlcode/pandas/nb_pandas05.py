# %%
import numpy as np
import pandas as pd
np.__version__, pd.__version__

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
# Planets Data
import seaborn as sns
planets = sns.load_dataset('planets')
planets.shape

# %%
planets.head()

# %%
planets.dropna().describe()


# %%
# Aggregation and Grouping
# Simple Aggregation in Pandas
rng = np.random.RandomState(42)
ser = pd.Series(rng.rand(5))
ser

# %%
print('mean:', ser.mean())
print('sum:', ser.sum())

# %%
df = pd.DataFrame({'A': rng.rand(5), 'B': rng.rand(5)})
df

# %%
df.mean()

# %%
df.mean(axis='columns')

# %%
# GroupBy: Split, Apply, Combine
df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'data': range(6)}, columns=['key', 'data'])
df

# %%
df.groupby('key').sum()

# %%
# The GroupBy object
# Column indexing
planets.groupby('method')['orbital_period'].median()

# %%
# Iteration over groups
for (method, group) in planets.groupby('method'):
    print("{0:30s} shape={1}".format(method, group.shape))

# %%
# Dispatch methods
planets.groupby('method')['year'].describe()


# %%
# Aggregate, filter, transform, apply
rng = np.random.RandomState(0)
df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'data1': range(6),
                   'data2': rng.randint(0, 10, 6)},
                  columns=['key', 'data1', 'data2'])
df

# %%
# Aggregation
df.groupby('key').aggregate(['min', np.median, max])

# %%
df.groupby('key').aggregate({'data1': 'min', 'data2': 'max'})

# %%
# Filtering
def filter_func(x):
    return x['data2'].std() > 4

display('df', "df.groupby('key').std()",
        "df.groupby('key').filter(filter_func)")

# %%
# Transformation
display('df', "df.groupby('key').transform(lambda x: x - x.mean())")

# %%
def trans_fn(x):
    # print(x)
    return x - x.mean()

df.groupby('key').transform(trans_fn)

# %%
# The apply() method
def norm_by_data2(x):
    # "x" is a DataFrame of group values
    # print(x)
    x['data1'] /= x['data2'].sum()
    return x

display('df', "df.groupby('key').apply(norm_by_data2)")


# %%
# Specifying the split key
L = [0, 1, 0, 1, 2, 0]
display('df', 'df.groupby(L).sum()')

# %%
display('df', "df.groupby(df['key']).sum()")

# %%
# A dictionary or series mapping index to group
df2 = df.set_index('key')
mapping = {'A': 'vowel', 'B': 'consonant', 'C': 'consonant'}
display('df2', 'df2.groupby(mapping).sum()')

# %%
# Any Python function
display('df2', 'df2.groupby(str.lower).mean()')

# %%
# Grouping example
decade = 10 * (planets['year'] // 10)
decade = decade.astype(str) + 's'
decade.name = 'decade'
decade.head()

# %%
planets.groupby(['method', decade])['number'].sum().unstack().fillna(0)


# %%
# Pivot Tables
# Motivating Pivot Tables
import seaborn as sns
titanic = sns.load_dataset('titanic')
titanic.shape

# %%
titanic.head()

# %%
# Pivot Tables by Hand
titanic.groupby('sex')[['survived']].mean()

# %%
titanic.groupby(['sex', 'class'])['survived'].aggregate('mean').unstack()

# %%
# Pivot Table Syntax
titanic.pivot_table('survived', index='sex', columns='class')

# %%
# Multi-level pivot tables
age = pd.cut(titanic['age'], [0, 18, 80])
titanic.pivot_table('survived', ['sex', age], 'class')

# %%
fare = pd.qcut(titanic['fare'], 2)
titanic.pivot_table('survived', ['sex', age], [fare, 'class'])

# %%
# Additional pivot table options
titanic.pivot_table(index='sex', columns='class',
                    aggfunc={'survived': sum, 'fare': 'mean'})

# %%
titanic.pivot_table('survived', index='sex', columns='class', margins=True)


# %%
# Example: Birthrate Data
births = pd.read_csv('data/births.csv')
births.head()

# %%
births['decade'] = 10 * (births['year'] // 10)
births.pivot_table('births', index='decade', columns='gender', aggfunc='sum')

# %%
%matplotlib inline
import matplotlib.pyplot as plt
sns.set()
births.pivot_table('births', index='year',
                   columns='gender', aggfunc='sum').plot()
plt.ylabel('total births per year')

# %%
print('pandas demo done')
