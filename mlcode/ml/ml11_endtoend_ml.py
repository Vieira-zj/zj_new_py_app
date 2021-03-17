# %%
# 实例：房价预测
# 检查数据
import pandas as pd

housing_path = 'data/housing.csv'
housing = pd.read_csv(housing_path)
print(housing.shape)
housing.head()

# %%
housing.info()

# %%
housing.describe()

# %%
# 数据可视化
%matplotlib inline
import matplotlib.pyplot as plt
housing.hist(bins=50, figsize=(20, 15))


# %%
# 切分训练集和测试集（纯随机的取样方法）
import numpy as np

def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

train_set, test_set = split_train_test(housing, 0.2)
train_set.shape, test_set.shape

# %%
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
train_set.shape, test_set.shape


# %%
# 查看收入分布矩形图
import matplotlib.pyplot as plt

def show_hist(df, col):
    plt.figure(figsize=(10, 6))
    plt.hist(df[col], bins=50, label=['income_category'])
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Income_Value')
    plt.ylabel('population')
    plt.show()

# %%
show_hist(housing, col='median_income')

# %%
import numpy as np
housing['income_cat'] = np.ceil(housing['median_income'] / 1.5)
housing['income_cat'].where(housing['income_cat'] < 5, 5.0, inplace=True)
show_hist(housing, col='income_cat')

# %%
# 根据收入分类，进行分层采样
from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing['income_cat']):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
strat_train_set.shape, strat_test_set.shape

# %%
# 删除income_cat属性
for set in (strat_train_set, strat_test_set):
    set.drop(['income_cat'], axis=1, inplace=True)
list(strat_train_set)


# %%
# 查看相关性
corr_matrix = housing.corr()
corr_matrix['median_house_value'].sort_values(ascending=False)

# %%
# 查看两两属性相关系分析图
%matplotlib inline
from pandas.plotting import scatter_matrix
attributes = ['median_house_value', 'median_income',
              'total_rooms', 'housing_median_age']
scatter_matrix(housing[attributes], figsize=(12, 8))

# %%
# 查看 房价 和 收入 的关系图
housing.plot(figsize=(8, 6), kind='scatter', x='median_income',
             y='median_house_value', alpha=0.25)

# %%
# 组合属性
housing['rooms_per_household'] = housing['total_rooms'] / housing['households']
housing['bedrooms_per_room'] = housing['total_bedrooms'] / housing['total_rooms']
housing['population_per_household'] = housing['population']/housing['households']

corr_matrix = housing.corr()
corr_matrix['median_house_value'].sort_values(ascending=False)


# %%
# 处理文本和类别属性
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
housing_cat = housing['ocean_proximity']
housing_cat_encoded = encoder.fit_transform(housing_cat)
print(type(housing_cat_encoded))
housing_cat_encoded[:5]

# %%
# one-hot 编码
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1,1))
print(type(housing_cat_1hot))
housing_cat_1hot.toarray()[:5]

# %%
# LabelEncoder + OneHotEncoder
from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
housing_cat_1hot = encoder.fit_transform(housing_cat)
housing_cat_1hot[:5]


# %%
# 数据准备 pipeline
housing_raw = strat_train_set.drop('median_house_value', axis=1)
housing_labels = strat_train_set['median_house_value'].copy()
housing_raw.shape, housing_labels.shape

# %%
housing_num = housing_raw.drop('ocean_proximity', axis=1)
num_attribs = list(housing_num)
cat_attribs = ['ocean_proximity']
num_attribs

# %%
# 添加一个特征组合的装换器
from sklearn.base import BaseEstimator, TransformerMixin
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        # nothing else to do
        return self
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            # np.c_表示的是拼接数组
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

# %%
# 选择对应的属性，将输出DataFrame转变成一个NumPy数组
from sklearn.base import BaseEstimator, TransformerMixin
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values

# %%
# https://stackoverflow.com/questions/40097177/pipeline-doesnt-work-with-label-encoder
from sklearn.preprocessing import LabelBinarizer

class MyLEncoder():
    def fit(self, X, y=None, **fit_params):
        return self
    def transform(self, X, y=None, **fit_params):
        enc = LabelBinarizer()
        encc = enc.fit(X)
        enc_data = enc.transform(X)
        return enc_data
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

# %%
# union pipeline
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', SimpleImputer(strategy='median')),  # 处理缺失值
    ('attribs_adder', CombinedAttributesAdder(
        add_bedrooms_per_room=False)),  # 特征组合
    ('std_scaler', StandardScaler()),  # 特征缩放
])

cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('label_binarizer', MyLEncoder()),
])

full_pipeline = FeatureUnion(transformer_list=[
    ('num_pipeline', num_pipeline),
    ('cat_pipeline', cat_pipeline),
])

housing_prepared = full_pipeline.fit_transform(housing_raw)
type(housing_prepared), housing_prepared.shape


# %%
# 训练一个线性回归模型
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

lin_reg = LinearRegression() 
lin_reg.fit(housing_prepared, housing_labels)

housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
lin_rmse

# %%
# 决策树
from sklearn.tree import DecisionTreeRegressor
tree_reg = DecisionTreeRegressor() 
tree_reg.fit(housing_prepared, housing_labels)

housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
tree_rmse


# %%
# 交叉验证集
def display_scores(scores):
    print('Scores:', scores)
    print('Mean:', scores.mean())
    print('Standard deviation:', scores.std())

# %%
# 决策树
from sklearn.model_selection import cross_val_score
tree_scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                              scoring='neg_mean_squared_error', cv=10)
tree_rmse_scores = np.sqrt(-tree_scores)
display_scores(tree_rmse_scores)

# %%
# 线性模型
lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,
                             scoring='neg_mean_squared_error', cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
display_scores(lin_rmse_scores)

# %%
# 随机森林
# cost some time
from sklearn.ensemble import RandomForestRegressor
forest_reg = RandomForestRegressor()
# forest_reg.fit(housing_prepared, housing_labels)
forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                scoring='neg_mean_squared_error', cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)
display_scores(forest_rmse_scores)


# %%
# 参数调节
from sklearn.model_selection import GridSearchCV

param_grid = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
]
forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid,
                           cv=5, scoring='neg_mean_squared_error')
grid_search.fit(housing_prepared, housing_labels)

cvres = grid_search.cv_results_
for mean_score, params in zip(cvres['mean_test_score'], cvres['params']):
    print(np.sqrt(-mean_score), params)

# %%
# 最优参数
grid_search.best_params_

# %%
# 测试集上对模型进行评估
final_model = grid_search.best_estimator_

X_test = strat_test_set.drop('median_house_value', axis=1)
y_test = strat_test_set['median_house_value'].copy()
X_test_prepared = full_pipeline.transform(X_test)
print(type(X_test_prepared), X_test_prepared.shape)

final_predictions = final_model.predict(X_test_prepared)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)
final_rmse


# %%
# 补充
# hist() 柱状图
import numpy as np
import pandas as pd
range1 = pd.Series(np.arange(100))
range2 = pd.Series(np.random.randint(0, 100, size=100))
df = pd.DataFrame({'range1': range1, 'range2': range2})
df.head()

# %%
%matplotlib inline
import matplotlib.pyplot as plt
df.hist(bins=10, figsize=(20, 15))
plt.show()

# %%
# filter condition
scope = pd.Series(np.arange(10))
label = pd.Series(np.random.choice(['x', 'y'], size=10))
df = pd.DataFrame({'scope': scope, 'label': label})
df

# %%
cond = df['scope'] % 2 == 0
print(df.loc[cond])
print()
print(df.loc[~cond])

# %%
cond = df['label'] == 'y'
print(df.loc[cond])
print()
print(df.loc[~cond])

# %%
print('end to end ml demo done')
