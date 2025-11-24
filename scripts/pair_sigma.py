# Plot an accurate fit for the synchrotron kernel F(x) and a simple heuristic approximation.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

sigma_T = 1.

def beta_star(x):
    return np.sqrt(...)

def sigma_pp(x):
    bs = beta_star(x)
    sigma = 3. / 16. * sigma_T * (1. - bs**2.)
    F = 2. * bs * (bs**2. - 2.) + (3. - bs**4.) * np.log((1. + bs) / (1. - bs))
    return sigma * F

# Set up figure
fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

# Axes limits
ax.set_xlim(1e-3, 1e3)
ax.set_ylim(1e-3, 1e1)

x = np.logspace(-4, 4, 1000) # E_gamma \epsilon
s_KN = sigma_KN(x)
x_hi = np.logspace(0, 4, 1000)
s_hi = sigma_high(x_hi)

ax.loglog(x, s_KN, lw=5, label=r" ")
ax.loglog(x_hi, s_hi, lw=3, ls=':', label=r" ")

ax.hlines(1., 1e-4, 1e4, ls=':', color='tab:gray')
#ax.text(0.19, 1e-3, r'$\nu_{\rm max}$', rotation=90, color='tab:gray')
ax.set_xlabel(r'$x \,=\, \epsilon/m_e c^2$')
ax.set_ylabel(r'$\sigma_{\rm KN}(x) \,/\, \sigma_{\rm T}$')
#ax.legend(loc="lower left")
#ax.grid(True, which="both")

out_path = "sigma_pair.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=200)
