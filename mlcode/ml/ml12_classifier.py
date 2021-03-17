#%%
# 数据集
# ${PIP_HOME}/tensorflow_core/python/keras/datasets/mnist.py
# path = os.path.join(os.getenv('PYPATH'), 'mlcode/dl/data/mnist.npz')
#
import tensorflow as tf
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 训练集
print(x_train.shape, y_train.shape)
# 测试集
print(x_test.shape, y_test.shape)

# %%
# 显示其中一个数字
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt

some_digit = x_train[36000]
plt.imshow(some_digit, cmap=mpl.cm.binary, interpolation='nearest')
plt.axis('off')
plt.show()

# %%
# show label
y_train[36000]


# %%
# 二元分类器
# 训练模型识别一个样本是否为9, 即有9和非9两类
y_train_9 = (y_train == 9)
y_test_9 = (y_test == 9)
y_train_9[:5], y_test_9[:5]

# %%
x_train = x_train.reshape(60000, -1)
x_train.shape

# %%
# 模型训练
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(x_train, y_train_9)

# %%
# 模型预测
some_digit = some_digit.reshape(1, -1)
print(some_digit.shape)
sgd_clf.predict(some_digit)

# %%
x_test = x_test.reshape(10000, -1)
print(x_test.shape)
sgd_clf.score(x_test, y_test_9)


# %%
# 交叉验证
from sklearn.model_selection import cross_val_score
sgd_clf = SGDClassifier(random_state=46)
cross_val_score(sgd_clf, x_train, y_train_9, cv=3, scoring='accuracy')

# %%
# 训练集中数字9的比例较少, 只有10%
import pandas as pd
pd.Series(y_train_9).value_counts()

# %%
from sklearn.base import BaseEstimator
import numpy as np

class ZeroClassifier(BaseEstimator):
    def fit(self, X, y=None):
        pass
    def predict(self, X):
        return np.zeros((len(X), 1), dtype=bool)

zero_clf = ZeroClassifier()
cross_val_score(zero_clf, x_train, y_train_9, cv=3, scoring='accuracy')

# %%
# 实现cross_val_score()
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone

def my_cross_val_score(clf, x_train, y_train, cv):
    skfolds = StratifiedKFold(n_splits=cv, random_state=42)
    for train_index, test_index in skfolds.split(x_train, y_train):
        clone_clf = clone(clf)
        x_train_folds = x_train[train_index]
        y_train_folds = y_train[train_index]
        x_test_fold = x_train[test_index]
        y_test_fold = y_train[test_index]

        clone_clf.fit(x_train_folds, y_train_folds)
        y_pred = clone_clf.predict(x_test_fold)
        n_correct = sum(y_pred == y_test_fold)
        print('accuracy:', (n_correct / len(y_pred)))

my_cross_val_score(sgd_clf, x_train, y_train_9, cv=3)


# %%
# 混淆矩阵
from sklearn.model_selection import cross_val_predict
y_train_predict = cross_val_predict(sgd_clf, x_train, y_train_9, cv=3)
print(y_train_predict.shape)
y_train_predict[:5]

# %%
from sklearn.metrics import confusion_matrix
confusion_matrix(y_train_9, y_train_predict)

# %%
from sklearn.metrics import precision_score, recall_score, f1_score
print('precision_score:', precision_score(y_train_9, y_train_predict))
print('recall_score:', recall_score(y_train_9, y_train_predict))
print('f1_score:', f1_score(y_train_9, y_train_predict))


# %%
# 精度与召回率
from sklearn.model_selection import cross_val_predict
# 之前使用cross_val_predict直接得出了预测的类别, 这里通过指定method参数, 算出每个样本的预测分数
y_scores = cross_val_predict(
    sgd_clf, x_train, y_train_9, cv=3, method='decision_function')
print(y_scores.shape)
y_scores[:5]

# %%
from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_train_9, y_scores)
precisions.shape, recalls.shape, thresholds.shape

# %%
# 精度与召回率的关系曲线
# 提高阈值, 精度上升而召回率下降, 降低阈值则会增加召回率而降低精度
import matplotlib.pyplot as plt

def plot_precision_recall_curve(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], 'b--', label='Precision')
    plt.plot(thresholds, recalls[:-1], 'g--', label='Recall')
    plt.xlabel('Threshold')
    plt.legend(loc='upper left')
    plt.ylim([0, 1])

plot_precision_recall_curve(precisions, recalls, thresholds)
plt.show()

# %%
# 精度和召回率函数图
def plot_precision_vs_recall(precisions, recalls):
    plt.plot(recalls, precisions, 'b--', linewidth=2)
    plt.xlabel('Recall', fontsize=16)
    plt.ylabel('Precision', fontsize=16)
    plt.axis([0, 1, 0, 1])
    plt.show()

plt.figure(figsize=(8, 6))
plot_precision_vs_recall(precisions, recalls)


# %%
# ROC曲线
from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_train_9, y_scores)

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)

plt.figure(figsize=(8, 6))
plot_roc_curve(fpr, tpr)
plt.show()


# %%
# 使用RandomForest训练一个分类器, 与前面SGD分类器进行比较
from sklearn.ensemble import RandomForestClassifier
forest_clf = RandomForestClassifier(n_estimators=10, random_state=42)
y_probas_forest = cross_val_predict(
    forest_clf, x_train, y_train_9, cv=3, method='predict_proba')
print(y_probas_forest.shape)

y_scores_forest = y_probas_forest[:, 1]  # 取正类的概率
y_scores_forest[:5]

# %%
fpr_forest, tpr_forest, thresholds_forest = roc_curve(
    y_train_9, y_scores_forest)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, 'b:', linewidth=2, label='SGD')
plot_roc_curve(fpr_forest, tpr_forest, 'Random Forest')
plt.legend(loc='lower right', fontsize=16)
plt.show()

# %%
from sklearn.metrics import roc_auc_score
roc_auc_score(y_train_9, y_scores_forest)

# %%
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_score, recall_score

y_train_pred_forest = cross_val_predict(forest_clf, x_train, y_train_9, cv=3)
print('precision_score:', precision_score(y_train_9, y_train_pred_forest))
print('recall_score:', recall_score(y_train_9, y_train_pred_forest))


# %%
# 多类别分类器
from sklearn.ensemble import RandomForestClassifier
forest_clf = RandomForestClassifier(n_estimators=10, random_state=46)
forest_clf.fit(x_train, y_train)

# %%
forest_clf.predict(some_digit)

# %%
print(forest_clf.classes_)
forest_clf.predict_proba(some_digit)

# %%
# 使用交叉验证评估多分类的分类器
cross_val_score(forest_clf, x_train, y_train, cv=3, scoring='accuracy')


# %%
# 多分类的混淆矩阵
y_train_pred = cross_val_predict(forest_clf, x_train, y_train, cv=3)
conf_mx = confusion_matrix(y_train, y_train_pred)
conf_mx

# %%
# 使用图型查看
plt.imshow(conf_mx, cmap=plt.cm.gray)
plt.colorbar()


# %%
# 分析单个错误
cl_a, cl_b = 3, 5
x_aa = x_train[(y_train == cl_a) & (y_train_pred == cl_a)]
x_ab = x_train[(y_train == cl_a) & (y_train_pred == cl_b)]
x_ba = x_train[(y_train == cl_b) & (y_train_pred == cl_a)]
x_bb = x_train[(y_train == cl_b) & (y_train_pred == cl_b)]
print(x_aa.shape, x_bb.shape)
print(x_ab.shape, x_ba.shape)

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_digits(instances, images_per_row=10, **options):
    size = 28
    images_per_row = min(len(instances), images_per_row)
    images = [instance.reshape(size, size) for instance in instances]
    n_rows = (len(instances) - 1) // images_per_row + 1
    row_images = []
    n_empty = n_rows * images_per_row - len(instances)
    images.append(np.zeros((size, size * n_empty)))
    for row in range(n_rows):
        rimages = images[row * images_per_row: (row + 1) * images_per_row]
        row_images.append(np.concatenate(rimages, axis=1))
    image = np.concatenate(row_images, axis=0)
    plt.imshow(image, cmap=mpl.cm.binary, **options)
    plt.axis('off')

# %%
plt.figure(figsize=(8, 8))
plt.subplot(221)
plot_digits(x_aa[:25], images_per_row=5)
plt.subplot(222)
plot_digits(x_ab[:25], images_per_row=5)
plt.subplot(223)
plot_digits(x_ba[:25], images_per_row=5)
plt.subplot(224)
plot_digits(x_bb[:25], images_per_row=5)
plt.show()


# %%
# 照片去除噪点
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_digit(some_digit):
    some_digit = some_digit.reshape(28, 28)
    plt.imshow(some_digit, cmap=mpl.cm.binary, interpolation='nearest')
    plt.axis('off')
    plt.show()

# %%
import numpy as np
x_train = x_train.reshape(60000, -1)
noise = np.random.randint(0, 100, (len(x_train), 784))
x_train_mod = x_train + noise

x_test = x_test.reshape(10000, -1)
noise = np.random.randint(0, 100, (len(x_test), 784))
x_test_mod = x_test + noise

y_train_mod = x_train
y_test_mod = x_test

some_index = 5500
plt.subplot(221)
plot_digit(x_test_mod[some_index])
plt.subplot(222)
plot_digit(y_test_mod[some_index])

# %%
from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier()

knn_clf.fit(x_train_mod, y_train_mod)
clean_digit = knn_clf.predict([x_test_mod[some_index]])
plot_digit(clean_digit)

# %%
print('Classifier demo end')
