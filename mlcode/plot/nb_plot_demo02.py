# %%
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('classic')

# %%
# Customizing Plot Legends
x = np.linspace(0, 10, 1000)
x.shape

# %%
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), '-b', label='Sine')
ax.plot(x, np.cos(x), '--r', label='Cosine')
ax.axis('equal')
ax.legend()

# %%
ax.legend(loc='upper left', frameon=False)
fig

# %%
ax.legend(frameon=False, loc='lower center', ncol=2)
fig

# %%
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
fig

# %%
# Choosing Elements for the Legend
y = np.sin(x[:, np.newaxis] + np.pi * np.arange(0, 2, 0.5))
y.shape

# %%
lines = plt.plot(x, y)
plt.legend(lines[:2], ['first', 'second'])

# %%
plt.plot(x, y[:, 0], label='first')
plt.plot(x, y[:, 1], label='second')
plt.plot(x, y[:, 2:])
plt.legend(framealpha=1, frameon=True)

# %%
# Multiple Legends
fig, ax = plt.subplots()

lines = []
styles = ['-', '--', '-.', ':']
x = np.linspace(0, 10, 1000)

for i in range(4):
    y = np.sin(x - i * np.pi / 2)
    lines += ax.plot(x, y, styles[i], color='black')
ax.axis('equal')

# specify the lines and labels of the first legend
ax.legend(lines[:2], ['line A', 'line B'],
          loc='upper right', frameon=False)

# create the second legend and add the artist manually
from matplotlib.legend import Legend
leg = Legend(ax, lines[2:], ['line C', 'line D'],
             loc='lower right', frameon=False)
ax.add_artist(leg)


# %%
# Customizing Colorbars
import numpy as np
np.random.seed(66)
import matplotlib.pyplot as plt
plt.style.use('classic')
%matplotlib inline

# %%
x = np.linspace(0, 10, 1000)
I = np.sin(x) * np.cos(x[:, np.newaxis])
I.shape

# %%
plt.imshow(I)
plt.colorbar()

# %%
# Customizing Colorbars
plt.imshow(I, cmap='gray')

# %%
from matplotlib.colors import LinearSegmentedColormap

def grayscale_cmap(cmap):
    '''Return a grayscale version of the given colormap'''
    cmap = plt.cm.get_cmap(cmap)
    colors = cmap(np.arange(cmap.N))

    RGB_weight = [0.299, 0.587, 0.114]
    luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weight))
    colors[:, :3] = luminance[:, np.newaxis]

    return LinearSegmentedColormap.from_list(cmap.name + '_gray', colors, cmap.N)

def view_colormap(cmap):
    '''Plot a colormap with its grayscale equivalent'''
    cmap = plt.cm.get_cmap(cmap)
    colors = cmap(np.arange(cmap.N))

    cmap = grayscale_cmap(cmap)
    grayscale = cmap(np.arange(cmap.N))

    fig, ax = plt.subplots(2, figsize=(6, 2),
                           subplot_kw=dict(xticks=[], yticks=[]))
    ax[0].imshow([colors], extent=[0, 10, 0, 1])
    ax[1].imshow([grayscale], extent=[0, 10, 0, 1])

# %%
view_colormap('jet')

# %%
view_colormap('viridis')

# %%
view_colormap('cubehelix')

# %%
view_colormap('RdBu')

# %%
# Example: Handwritten Digits
from sklearn.datasets import load_digits
digits = load_digits(n_class=6)

fig, ax = plt.subplots(8, 8, figsize=(6, 6))
for i, axi in enumerate(ax.flat):
    axi.imshow(digits.images[i], cmap='binary')
    axi.set(xticks=[], yticks=[])


# %%
# Multiple Subplots
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

# %%
# plt.axes: Subplots by Hand
ax1 = plt.axes()
# [left, bottom, width, height]
ax2 = plt.axes([0.65, 0.65, 0.2, 0.2])

# %%
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.5, 0.8, 0.4],
                   xticklabels=[], ylim=(-1.2, 1.2))
ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.4],
                   ylim=(-1.2, 1.2))

x = np.linspace(0, 10)
ax1.plot(np.sin(x))
ax2.plot(np.cos(x))

# %%
# plt.subplot: Simple Grids of Subplots
for i in range(1, 7):
    plt.subplot(2, 3, i)
    plt.text(0.5, 0.5, str((2, 3, i)), fontsize=18, ha='center')

# %%
fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
for i in range(1, 7):
    ax = fig.add_subplot(2, 3, i)
    ax.text(0.5, 0.5, str((2, 3, i)), fontsize=18, ha='center')

# %%
# plt.subplots: The Whole Grid in One Go
fig, ax = plt.subplots(2, 3, sharex='col', sharey='row')

# %%
# axes are in a two-dimensional array, indexed by [row, col]
for i in range(2):
    for j in range(3):
        ax[i, j].text(0.5, 0.5, str((i, j)), fontsize=18, ha='center')
fig

# %%
# plt.GridSpec: More Complicated Arrangements
grid = plt.GridSpec(2, 3, wspace=0.4, hspace=0.3)
plt.subplot(grid[0, 0])
plt.subplot(grid[0, 1:])
plt.subplot(grid[1, :2])
plt.subplot(grid[1, 2])

# %%
# Create some normally distributed data
mean = [0, 0]
cov = [[1, 1], [1, 2]]
x, y = np.random.multivariate_normal(mean, cov, 3000).T

# Set up the axes with gridspec
fig = plt.figure(figsize=(6, 6))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[:-1, 1:])
y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)

# scatter points on the main axes
main_ax.plot(x, y, 'ok', markersize=3, alpha=0.2)
# histogram on the attached axes
x_hist.hist(x, 40, histtype='stepfilled',
            orientation='vertical', color='gray')
x_hist.invert_yaxis()
y_hist.hist(y, 40, histtype='stepfilled',
            orientation='horizontal', color='gray')
y_hist.invert_xaxis()


# %%
# Text and Annotation
import numpy as np
import pandas as pd
np.random.seed(66)

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-whitegrid')

# %%
births = pd.read_csv('data/births.csv')
quartiles = np.percentile(births['births'], [25, 50, 75])
mu, sig = quartiles[1], 0.74 * (quartiles[2] - quartiles[0])
births = births.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
births.head()

# %%
births['day'] = births['day'].astype(int)
births.index = pd.to_datetime(10000 * births.year +
                              100 * births.month +
                              births.day, format='%Y%m%d')

births_by_date = births.pivot_table('births',
                                    [births.index.month, births.index.day])
births_by_date.index = [pd.datetime(2012, month, day)
                        for (month, day) in births_by_date.index]
births_by_date.head()

# %%
fig, ax = plt.subplots(figsize=(12, 4))
births_by_date.plot(ax=ax)

# %%
fig, ax = plt.subplots(figsize=(12, 4))
births_by_date.plot(ax=ax)

# Add labels to the plot
style = dict(size=10, color='gray')

ax.text('2012-1-1', 3950, "New Year's Day", **style)
ax.text('2012-7-4', 4250, 'Independence Day', ha='center', **style)
ax.text('2012-9-4', 4850, 'Labor Day', ha='center', **style)
ax.text('2012-10-31', 4600, 'Halloween', ha='right', **style)
ax.text('2012-11-25', 4450, 'Thanksgiving', ha='center', **style)
ax.text('2012-12-25', 3850, 'Christmas', ha='right', **style)

# Label the axes
ax.set(title='USA births by day of year (1969-1988)',
       ylabel='average daily births')

# Format the x axis with centered month labels
ax.xaxis.set_major_locator(mpl.dates.MonthLocator())
ax.xaxis.set_minor_locator(mpl.dates.MonthLocator(bymonthday=15))
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.xaxis.set_minor_formatter(mpl.dates.DateFormatter('%h'))

# %%
# Transforms and Text Position
fig, ax = plt.subplots(facecolor='lightgray')
ax.axis([0, 10, 0, 10])

# transform=ax.transData is the default, but we'll specify it anyway
ax.text(1, 5, '. Data: (1, 5)', transform=ax.transData)
ax.text(0.5, 0.1, '. Axes: (0.5, 0.1)', transform=ax.transAxes)
ax.text(0.2, 0.2, '. Figure: (0.2, 0.2)', transform=fig.transFigure)

# %%
ax.set_xlim(0, 2)
ax.set_ylim(-6, 6)
fig

# %%
# Arrows and Annotation
%matplotlib inline
fig, ax = plt.subplots()

x = np.linspace(0, 20, 1000)
ax.plot(x, np.cos(x))
ax.axis('equal')

ax.annotate('local maximum', xy=(6.28, 1), xytext=(10, 4),
            arrowprops=dict(facecolor='black', shrink=0.05))
ax.annotate('local minimum', xy=(5 * np.pi, -1), xytext=(2, -6),
            arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=-90"))

# %%
print('plot demo done')
