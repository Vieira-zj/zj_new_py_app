# %%
import numpy as np
np.random.seed(66)
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# %%
# Simple Line Plots
# 画布
fig = plt.figure()
# 绘图区
ax = plt.axes()

x = np.linspace(0, 10, 1000)
ax.plot(x, np.sin(x))

# %%
plt.plot(x, np.sin(x))

# %%
plt.plot(x, np.sin(x))
plt.plot(x, np.cos(x))

# %%
# Adjusting the Plot: Line Colors and Styles
# specify color by name
plt.plot(x, np.sin(x - 0), color='blue')
# short color code (rgbcmyk)
plt.plot(x, np.sin(x - 1), color='g')
# Grayscale between 0 and 1
plt.plot(x, np.sin(x - 2), color='0.75')
# Hex code (RRGGBB from 00 to FF)
plt.plot(x, np.sin(x - 3), color='#FFDD44')
# RGB tuple, values 0 to 1
plt.plot(x, np.sin(x - 4), color=(1.0, 0.2, 0.3))
# all HTML color names supported
plt.plot(x, np.sin(x - 5), color='chartreuse')

# %%
plt.plot(x, x + 0, linestyle='solid')
plt.plot(x, x + 1, linestyle='dashed')
plt.plot(x, x + 2, linestyle='dashdot')
plt.plot(x, x + 3, linestyle='dotted')

# %%
# For short, you can use the following codes
plt.plot(x, x + 4, linestyle='-')  # solid
plt.plot(x, x + 5, linestyle='--')  # dashed
plt.plot(x, x + 6, linestyle='-.')  # dashdot
plt.plot(x, x + 7, linestyle=':')  # dotted

# %%
# Adjusting the Plot: Axes Limits
plt.plot(x, np.sin(x))
plt.xlim(-1, 11)
plt.ylim(-1.5, 1.5)

# %%
plt.plot(x, np.sin(x))
plt.xlim(10, 0)
plt.ylim(1.2, -1.2)

# %%
plt.plot(x, np.sin(x))
plt.axis([-1, 11, -1.5, 1.5])

# %%
plt.plot(x, np.sin(x))
plt.axis('tight')

# %%
plt.plot(x, np.sin(x))
plt.axis('equal')

# %%
# Labeling Plots
plt.plot(x, np.sin(x))
plt.title('A Sine Curve')
plt.xlabel('x')
plt.ylabel('sin(x)')

# %%
plt.plot(x, np.sin(x), '-g', label='sin(x)')
plt.plot(x, np.cos(x), ':b', label='cos(x)')
plt.axis('equal')
plt.legend()

# %%
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10), ylim=(-2, 2),
       xlabel='x', ylabel='sin(x)',
       title='A Simple Plot')


# %%
# Simple Scatter Plots
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# %%
x = np.linspace(0, 10, 30)
y = np.sin(x)
plt.plot(x, y, 'o', color='black')

# %%
rng = np.random.RandomState(0)
for marker in ['o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd']:
    plt.plot(rng.rand(5), rng.rand(5), marker,
             label="marker='{0}'".format(marker))
plt.legend(numpoints=1)
plt.xlim(0, 1.8)

# %%
plt.plot(x, y, '-ok')

# %%
plt.plot(x, y, '-p', color='gray',
         markersize=15, linewidth=4,
         markerfacecolor='white',
         markeredgecolor='gray',
         markeredgewidth=2)
plt.ylim(-1.2, 1.2)

# %%
# Scatter Plots with plt.scatter
plt.scatter(x, y, marker='o')

# %%
rng = np.random.RandomState(0)
x = rng.randn(100)
y = rng.randn(100)
colors = rng.rand(100)
sizes = 1000 * rng.rand(100)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.3, cmap='viridis')
plt.colorbar()  # show color scale

# %%
# plt.plot should be preferred over plt.scatter for large datasets.
# The reason is that plt.scatter has the capability to render a different size and/or color for each point,
# so the renderer must do the extra work of constructing each point individually.


# %%
# Visualizing Errors
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# %%
# Basic Errorbars
x = np.linspace(0, 10, 50)
dy = 0.8
y = np.sin(x) + dy * np.random.randn(50)
plt.errorbar(x, y, yerr=dy, fmt='.k')

# %%
plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
             ecolor='lightgray', elinewidth=3, capsize=0)


# %%
# Density and Contour Plots
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

# %%
# Visualizing a Three-Dimensional Function
def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

# %%
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)
Z.shape

# %%
plt.contour(X, Y, Z, colors='black')

# %%
plt.contour(X, Y, Z, 20, cmap='RdGy')

# %%
plt.contourf(X, Y, Z, 20, cmap='RdGy')
plt.colorbar()

# %%
plt.imshow(Z, extent=[0, 5, 0, 5], origin='lower', cmap='RdGy')
plt.colorbar()
plt.axis(aspect='image')

# %%
contours = plt.contour(X, Y, Z, 3, colors='black')
plt.clabel(contours, inline=True, fontsize=8)

plt.imshow(Z, extent=[0, 5, 0, 5], origin='lower',
           cmap='RdGy', alpha=0.5)
plt.colorbar()


# %%
# Histograms, Binnings, and Density
import numpy as np
np.random.seed(66)
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

# %%
data = np.random.randn(1000)
data[:5]

# %%
counts, bin_edges = np.histogram(data, bins=5)
counts, bin_edges

# %%
plt.hist(data)

# %%
plt.hist(data, bins=30, normed=True, alpha=0.5,
         histtype='stepfilled', color='steelblue',
         edgecolor='none')

# %%
x1 = np.random.normal(0, 0.8, 1000)
x2 = np.random.normal(-2, 1, 1000)
x3 = np.random.normal(3, 2, 1000)

kwargs = dict(histtype='stepfilled', alpha=0.3, normed=True, bins=40)
plt.hist(x1, **kwargs)
plt.hist(x2, **kwargs)
plt.hist(x3, **kwargs)

# %%
# Two-Dimensional Histograms and Binnings
mean = [0, 0]
cov = [[1, 1], [1, 2]]
x, y = np.random.multivariate_normal(mean, cov, 10000).T
x.shape, y.shape

# %%
plt.hist2d(x, y, bins=30, cmap='Blues')
cb = plt.colorbar()
cb.set_label('counts in bin')

# %%
counts, xedges, yedges = np.histogram2d(x, y, bins=30)
counts.shape

# %%
plt.hexbin(x, y, gridsize=30, cmap='Blues')
plt.colorbar(label='count in bin')

# %%
print('plot demo done')
