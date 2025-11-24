# Plot an accurate fit for the synchrotron kernel F(x) and a simple heuristic approximation.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

sigma_T = 1.

def beta_star(x):
    # x = s / 4 m_e c^4
    return np.sqrt(1. - 1. / x)

def sigma_pp(x):
    bs = beta_star(x)
    sigma = 3. / 16. * sigma_T * (1. - bs**2.)
    F = 2. * bs * (bs**2. - 2.) + (3. - bs**4.) * np.log((1. + bs) / (1. - bs))
    return sigma * F

# Set up figure
fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

# Axes limits
ax.set_xlim(0.4, 1e3)
ax.set_ylim(1e-3, 0.4)

x = np.logspace(0, 4, 10000)
y = sigma_pp(x)

id = (y == max(y))
print(x[id], y[id])

ax.loglog(x, y, lw=5, label=r" ")

ax.hlines(0.26, 0.1, 1e3, ls=':', color='tab:gray')
ax.vlines(2., 1e-3, 1, ls=':', color='tab:gray')
##ax.text(0.19, 1e-3, r'$\nu_{\rm max}$', rotation=90, color='tab:gray')
ax.set_xlabel(r'$x \,=\, s / 4 m_e^2 c^4$')
ax.set_ylabel(r'$\sigma_{\gamma\gamma}(x) \,/\, \sigma_{\rm T}$')
##ax.legend(loc="lower left")
##ax.grid(True, which="both")

out_path = "pair_sigma.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=200)
