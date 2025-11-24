# Plot an accurate fit for the synchrotron kernel F(x) and a simple heuristic approximation.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

sigma_T = 1.

def sigma_KN(x):
    sigma = 3. / 4. * sigma_T
    F = (1. + x) / x**3. * (2. * x * (1. + x) / (1. + 2. * x) - np.log(1. + 2. * x))
    F += 1. / 2. / x * np.log(1. + 2. * x)
    F -= (1. + 3. * x) / (1. + 2. * x)**2.
    return sigma * F

def sigma_approx(x):
    return 3. / 8. / x * (np.log(2. * x) + 0.5)

# Set up figure
fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

# Axes limits
ax.set_xlim(1e-3, 1e3)
ax.set_ylim(1e-3, 3)

x = np.logspace(-4, 4, 1000)
s_KN = sigma_KN(x)
s_approx = sigma_approx(x)

ax.loglog(x, s_KN, lw=5, label=r" ")
ax.loglog(x, s_approx, lw=3, ls=':', label=r" ")

ax.hlines(1., 1e-4, 1e4, ls=':', color='tab:gray')
#ax.text(0.19, 1e-3, r'$\nu_{\rm max}$', rotation=90, color='tab:gray')
ax.set_xlabel(r'$x \,=\, \epsilon/m_e c^2$')
ax.set_ylabel(r'$\sigma_{\rm KN}(x) \,/\, \sigma_{\rm T}$')
#ax.legend(loc="lower left")
#ax.grid(True, which="both")

out_path = "sigma_KN.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=200)
