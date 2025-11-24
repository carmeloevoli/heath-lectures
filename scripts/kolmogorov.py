# Retry: Kolmogorov turbulence cascade schematic with injection, inertial, and dissipation scales.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

fig = plt.figure(figsize=(15.5, 8.5))
ax = fig.add_subplot(111)

k = np.logspace(-2, 2, 1000)
k_L = 1e-1
k_d = 2e1
eps = 1.0
Ck = 1.5

E = np.zeros_like(k)
mask_forcing = k < k_L
mask_inertial = (k >= k_L) & (k <= k_d)
mask_diss = k > k_d

s = 0.25
E = (Ck*eps**(2/3)) * (k / k_L)**9 * np.power(0.5 * (1. + np.power(k / k_L, 1. / s)), (-9.0-5./3.) * s)
E *= np.exp(-(k/k_d)**3.0)
ax.loglog(k, E, lw=4.5, color='tab:orange')

ax.axvline(k_L, ls='--', lw=1.8, color='tab:blue')
ax.axvline(k_d, ls='--', lw=1.8, color='tab:green')

ax.text(k_L*0.9, 1.2e-3, r"Injection scale $L$ ($k_L = 2\pi/L$)", ha='right', va='center', rotation=90, fontsize=22, color='tab:blue')
ax.text(k_d*1.15, 4.5e-2, r"Dissipation scale $\ell_{\rm d}$ ($k_d = 2\pi/\ell_{\rm d}$)", ha='left', va='center', rotation=90, fontsize=22, color='tab:green')

x_mid = np.sqrt(k_L*k_d)
y_mid = (Ck*eps**(2/3))*(x_mid**(-5/3))

k_line = np.array([k_L*2.0, k_d/2.0])
E_line = 0.02 * y_mid*(k_line/x_mid)**(-5/3)
ax.loglog(k_line, E_line, lw=1.8, ls='--', color='tab:red')

ax.text(x_mid, y_mid*0.0048, r"Inertial range $k_L \gg k \gg k_d$", ha='center', va='bottom', fontsize=22, color='tab:red', rotation=-27.5)

ax.set_xlabel(r"Wavenumber $k$")
ax.set_ylabel(r"Energy spectrum $E(k)$")
ax.set_xlim(2. * k.min(), k.max())
#ax.set_ylim(E[E>0].min()*0.5, E.max()*4)
ax.set_ylim([1e-5, 1e1])

plt.tight_layout()
plt.savefig('kolmogorov_cascade_schematic.pdf', dpi=300, bbox_inches="tight")
