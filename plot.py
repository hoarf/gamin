
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(-2, 2, 0.25)
Y = np.arange(-2, 2, 0.25)
X, Y = np.meshgrid(X, Y)

Z = -X*np.sqrt(abs(X))-Y*np.sin(np.sqrt(abs(Y)))
R = 100*(Y-X**2)**2+(1-X)**2
W3 = R-Z

surf = ax.plot_surface(X, Y,W3, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.set_zlim(-2000, 4000)
ax.set_zlim3d(-2000, 4000)

ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()