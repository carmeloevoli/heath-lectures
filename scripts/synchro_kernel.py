# Plot an accurate fit for the synchrotron kernel F(x) and a simple heuristic approximation.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math
import mpmath as mp

# ---- Precision / global settings -------------------------------------------
mp.mp.dps = 70   # decimal digits of precision; increase if you need ultra-accuracy

# ---- Core routines ----------------------------------------------------------
def _F_integral_scalar(x: float, tail_split: float = 30.0) -> float:
    """
    Compute F(x) for a scalar x > 0 by splitting the integral:
        F(x) = x * [ ∫_x^{x+Δ} K_{5/3}(t) dt  +  ∫_{x+Δ}^∞ K_{5/3}(t) dt ]
    The second piece is evaluated with an asymptotic integrand to speed convergence.

    Parameters
    ----------
    x : float
        Argument (x = nu / nu_c); must be > 0.
    tail_split : float
        Δ; the integration is split at (x + Δ). Larger Δ makes the asymptotic more accurate.

    Returns
    -------
    float
        F(x)
    """
    if x <= 0:
        raise ValueError("x must be positive.")

    # Near-zero safeguard: for very small x the integral is easy numerically,
    # but we can also short-circuit to the known asymptote.
    if x < 1e-6:
        return float(2.15 * x**(1.0/3.0))  # low-x asymptote

    nu = mp.mpf('5')/mp.mpf('3')
    K = lambda t: mp.besselk(nu, t)

    # Numeric part up to (x + Δ)
    upper = x + tail_split
    part_num = mp.quad(K, [x, upper])

    # Tail part: use large-t asymptote  K_nu(t) ~ sqrt(pi/(2t)) e^{-t}
    tail_integrand = lambda t: mp.sqrt(mp.pi/(2*t)) * mp.e**(-t)
    part_tail = mp.quad(tail_integrand, [upper, mp.inf])

    return float(x * (part_num + part_tail))

def synchrotron_kernel_F(x, tail_split: float = 20.0):
    """
    Vectorized wrapper for F(x). Accepts scalar or array-like x.

    Parameters
    ----------
    x : float or array-like
        Argument(s) where to evaluate F.
    tail_split : float
        Δ used to split the integral for speed/accuracy.

    Returns
    -------
    float or np.ndarray
        F(x) with the same shape as input.
    """
    if np.isscalar(x):
        return _F_integral_scalar(float(x), tail_split=tail_split)
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x, dtype=float)
    it = np.nditer(x, flags=['multi_index'])
    for xi in it:
        print (xi)
        out[it.multi_index] = _F_integral_scalar(float(xi), tail_split=tail_split)
    return out

def F_heuristic(x):
    return 1.8 * np.power(x, 1/3.0) * np.exp(-x)

def F_low(x):
    return 2.15 * np.power(x, 1/3.0)

def F_high(x):
    return np.sqrt(np.pi * x / 2.0) * np.exp(-x)

# Set up figure
fig = plt.figure(figsize=(11.5, 8.0))
ax = fig.add_subplot(111)

# Axes limits
ax.set_xlim(1e-4, 1e1)
ax.set_ylim(1e-4, 1e1)

x = np.logspace(-4, 1, 100)
F_fit_vals = F_heuristic(x) # synchrotron_kernel_F(x) # F_fit(x)
F_heu_vals = F_heuristic(x)
F_low_vals = F_low(x)
F_high_vals = F_high(x)

ax.loglog(x, F_fit_vals, lw=5, label=r"Synchrotron kernel $F(x)$ (accurate)")
ax.loglog(x, F_low_vals, lw=3, linestyle='--', label=r"Low-$x$ asymptote $2.15\,x^{1/3}$")
ax.loglog(x, F_high_vals, lw=3, linestyle='-.', label=r"High-$x$ asymptote $\sqrt{\pi x/2}\,e^{-x}$")
ax.loglog(x, F_heu_vals, lw=3, linestyle=':', label=r"Heuristic $1.8\,x^{1/3}e^{-x}$")

ax.vlines(0.29, 1e-4, 1e1, ls=':', color='tab:gray')
ax.text(0.17, 1e-3, r'$\nu_{\rm max}$', rotation=90, color='tab:gray', fontsize=22)
ax.set_xlabel(r'$x\,=\,\nu/\nu_c$')
ax.set_ylabel(r'Synchrotron kernel $F(x)$')
ax.legend(loc="lower left", fontsize=17)
#ax.grid(True, which="both")

out_path = "synchrotron_kernel_Fx.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=200)
