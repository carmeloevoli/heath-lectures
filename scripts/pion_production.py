import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

def plot_sigmaPlus_data(ax, color):
    Tlab = [0.59, 0.73 , 2.85 , 7.91 , 11.1, 18.1, 23.1 , 68.1 , 101.1 , 204.1 , 302.1]
    sigma = [9.7, 13.5, 26.1, 39.9, 43.2, 47.5, 56.8, 81.5, 91.8, 108, 125]
    sigma_err = [1.2, 0.73, 5.0, 0.6, 0.9, 1.0, 0.9, 8.2, 9.2, 11, 13]
    ax.errorbar(Tlab, sigma, yerr=sigma_err,
        fmt='o', color=color, markeredgecolor=color,
        markersize=7, elinewidth=2, capsize=4, capthick=2, zorder=1)

def plot_sigmaMinus_data(ax, color):
    Tlab = [0.73 , 2.85 , 7.91 , 11.1, 18.1, 23.1, 68.1 , 101.1 , 204.1 , 302.1 ]
    sigma = [0.03, 6.0 , 19.1, 21.3 , 30, 33.8, 62.7, 66.9, 86, 99.5]
    sigma_err = [0.01 , 1.2 , 0.6 , 0.4 , 0.6, 0.6,1.0 , 1.3 , 2, 3.0]
    ax.errorbar(Tlab, sigma, yerr=sigma_err,
        fmt='o', color=color, markeredgecolor=color,
        markersize=7, elinewidth=2, capsize=4, capthick=2, zorder=2)

def plot_sigmaNo_data(ax, color):
    Tlab = [0.4, 11.1 , 18.1 , 23.1 , 68.1 , 101.1 , 204.1 , 299.1, 302.1, 399.1]
    sigma = [0.1, 31.5, 41.6, 53.5, 81.1, 85, 107.3, 130, 127, 142.3]
    sigma_err = [0.007 , 2.6 , 3.5 , 3.1 , 4, 8,  6.8 , 5, 12, 6.2]
    ax.errorbar(Tlab, sigma, yerr=sigma_err,
        fmt='o', color=color, markeredgecolor=color,
        markersize=7, elinewidth=2, capsize=4, capthick=2, zorder=3)

fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

#ax.set_xscale('log')
ax.set_xlim([0, 300.])
ax.set_xlabel(r'T$_{\rm lab}$ [GeV]')
#ax.set_yscale('log')
ax.set_ylabel(r'$\sigma$ (p+p$\rightarrow \pi + X)$')
ax.set_ylim([0., 120.])

Tlab = np.linspace(0, 500, 1000)
Tlab2 = Tlab * Tlab

sigmaPlus = 1. / (0.00717 + 0.0652 * np.log(Tlab) / Tlab + 0.162 / Tlab2)
ax.plot(Tlab, sigmaPlus, color='g', label=r'$\sigma_{\pi^+}$', zorder=1)
plot_sigmaPlus_data(ax, 'g')

sigmaMinus = 1. / (0.00456 + 0.0846 / np.power(Tlab, 0.5) + 0.577 / np.power(Tlab, 1.5))
ax.plot(Tlab, sigmaMinus, color='b', label=r'$\sigma_{\pi^-}$', zorder=2)
plot_sigmaMinus_data(ax, 'b')

sigmaNo = 1. / (0.007 + 0.1 * np.log(Tlab) / Tlab + 0.3 / Tlab2)
ax.plot(Tlab, sigmaNo, color='r', label=r'$\sigma_{\pi^0}$', zorder=3)
plot_sigmaNo_data(ax, 'r')

ax.plot(Tlab, 0.5 * (sigmaPlus + sigmaMinus), color='tab:gray', linestyle='--', label=r'$\frac{1}{2}(\sigma_{\pi^-} + \sigma_{\pi^+})$', zorder=10)

ax.legend(fontsize=24)
plt.savefig('pion_production.pdf')
