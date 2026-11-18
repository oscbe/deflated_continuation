import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 1000)
eps = 0.04

u_in_l = lambda x, y: 3*np.cosh(y*(1 - x)/(eps*(2**(1/2))) + np.arctanh((2/3)**(1/2)))**(-2)
u_in_r = lambda x, y: 3*np.cosh(y*(1 + x)/(eps*(2**(1/2))) + np.arctanh((2/3)**(1/2)))**(-2)

u_out = lambda x: x**2 - 1 - (1 + (1 - x**2)**2)**(1/2)


fig, axs = plt.subplots(2, 2, figsize=(15, 10))
for row, i in enumerate([1, -1]):
    for col, j in enumerate([1, -1]):
        ax = axs[row, col]
        ax.plot(x, u_in_l(x, i) + u_in_r(x, j) + u_out(x))
        ax.grid()
        ax.set_ylim(-3, 2)

        ax.set_xlabel('x', fontweight='bold')
        ax.set_ylabel('y', fontweight='bold')
fig.tight_layout()
plt.savefig('figs/approx_sols')