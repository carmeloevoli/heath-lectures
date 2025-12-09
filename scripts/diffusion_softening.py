import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

ax.set_ylabel(r'intensity')
ax.set_ylim([1e-2,2])
ax.set_yscale('log')
ax.set_xlabel(r'energy')
ax.set_xlim([1,1e3])
ax.set_xscale('log')

T = np.logspace(0, 3, 100)

ax.plot([10.,10.], [np.power(10. / T[0], -0.2), np.power(10. / T[0], -0.66)], color='tab:orange', linestyle=':', lw=3.5)

ax.text(10., .80, 'slow escape', color='tab:orange', fontsize=18, ha='center', va='center')

ax.plot([500.,500.], [np.power(500. / T[0], -0.2), np.power(500. / T[0], -0.66)], color='tab:orange', linestyle=':', lw=3.5)
ax.text(500., .35, 'fast escape', color='tab:orange', fontsize=18, ha='center', va='center')

ax.plot(T, np.power(T / T[0], -0.2), color='tab:red', label='injection', lw=4)
ax.plot(T, np.power(T / T[0], -0.66), color='tab:blue', label='after propagation', lw=4)

ax.text(70, 0.25, r'$E^{-\gamma}$', color='tab:red', fontsize=30)
ax.text(70, 0.02, r'$E^{-\gamma-\delta}$', color='tab:blue', fontsize=30)

ax.legend()
plt.savefig('diffusion_softening.pdf')
