import numpy as np
from pylab import meshgrid, cm, imshow, contour, clabel, colorbar, axis, title, show
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt


def pfun12(m, V):
    q1 = m - 1732.36430209377
    q2 = V - 4.20052519787045
    P = -45.952887494116 + 0.12308218418175*m + 0.09418974202318*V + \
        0.00018646959266*q1**2 + 0.00503179158534*q1*q2 - 0.4994068002927*q2**2
    return P


def pfun5(m, V):
    q1 = m - 1415.60258877997
    q2 = V - 4.09112359606267
    P = -95.593207832974 + 0.27069824534698*m + 5.09719902899635*V + \
        0.00098502759429*q1**2 + 0.00442224684513*q1*q2 + 0.59435253538876*q2**2
    return P


m12 = np.linspace(500, 1200, 100)
V12 = np.linspace(0, 5.5, 100)
mm12, VV12 = np.meshgrid(m12, V12)
print type(mm12)
print mm12

m5 = np.linspace(400, 1000, 700)
V5 = np.linspace(0, 5.5, 700)
mm5, VV5 = meshgrid(m5, V5)

P12 = pfun12(mm12, VV12)
P5 = pfun5(mm5, VV5)

# im12 = imshow(P12, cmap=cm.RdBu)
# cset = contour(P12, np.arange(P12.min(), P12.max(), 1), linewidths=1, cmap=cm.Set2)
# clabel(cset, inline=True, fmt='%1.1f', fontsize=10)
# colorbar(im12)
# show()

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(mm12, VV12, P12, rstride=1, cstride=1, cmap=cm.RdBu, linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()





