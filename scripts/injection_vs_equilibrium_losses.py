# Re-run: Create the plot of injection (delta & power law) and steady-state spectra under b(E) ~ E^2.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

# Set up figure
fig = plt.figure(figsize=(15.5, 10.5))
ax = fig.add_subplot(111)

# Energy grid
E = np.logspace(0, 5, 1000)

# Axes limits
ax.set_xlim(1e0, 1e4)
ax.set_ylim(1e-8, 1e0)

# Loss law parameters
m = 2.0
b0 = 1.0
b = b0 * E**m

# Delta-like injection at E_inj
E_inj = 1e3
Q0_delta = 1.0
sigma_log = 0.02
Q_delta = Q0_delta * np.exp(-0.5 * (np.log(E/E_inj)/sigma_log)**2) / (np.sqrt(2*np.pi)*sigma_log*E)

N_delta = np.where(E <= E_inj, Q0_delta / b, 0.0)

# Power-law injection between Emin and Emax
p = 2.2
Emin, Emax = 10.0, 1e5
Q0_pl = 1.0
Q_pl = np.where((E>=Emin) & (E<=Emax), Q0_pl * E**(-p), 0.0)

# Numerical steady state (no escape): N(E) = (1/b(E)) * ∫_E^∞ Q(E') dE'
rev_Q = Q_pl[::-1]
rev_E = E[::-1]
rev_cum = np.cumsum(0.5*(rev_Q[:-1] + rev_Q[1:]) * (rev_E[:-1] - rev_E[1:]))
cum_int = np.zeros_like(E)
cum_int[:-1] = rev_cum[::-1]
cum_int[-1] = 0.0
N_pl = cum_int / b

# Plot
ax.loglog(E, Q_delta, linestyle='--', linewidth=2, label='Injection: $Q=Q_0\\,\\delta(E-E_\\mathrm{inj})$')
#ax.loglog(E, Q_pl, linestyle=':', linewidth=1, label=rf'Injection: $Q \propto E^{{-{p}}}$ ($E_{{\rm min}}$–$E_{{\rm max}}$)')

ax.loglog(E, N_delta, linewidth=3, label='Equilibrium: $N(E)$ for $\\delta$-injection')
#ax.loglog(E, N_pl, linewidth=2, label='Equilibrium: $N(E)$ for power-law injection')

# Annotations for slopes
x_ann = 30
y_ann = (Q0_delta / (b0 * x_ann**m))
#ax.text(x_ann, y_ann*2.0, r'$N\propto E^{-m}\ (m=2)$', fontsize=19)

x_ann2 = 3e3
y_ann2 = np.interp(x_ann2, E, N_pl)
#ax.text(x_ann2, y_ann2*2.5, rf'$N\propto E^{{-(p+m-1)}}$ = $E^{{-( {p}+{m}-1 )}}$', fontsize=19, ha='center')

# Markers
#for x, lab in [(Emin, r'$E_{\rm min}$'), (E_inj, r'$E_{\rm inj}$'), (Emax, r'$E_{\rm max}$')]:
#    ax.axvline(x, linestyle='-', linewidth=0.8, alpha=0.5)
#    ax.text(x, ax.get_ylim()[0]*1.2, lab, rotation=90, va='bottom', ha='center', fontsize=18)

ax.set_xlabel('Energy $E$ (arb. units)')
ax.set_ylabel(r'Injection $Q(E)$ and equilibrium $N(E)$ (arb. units)')
ax.set_title('Injection vs. Equilibrium Spectra under Radiative Losses ($b\\propto E^2$)')
ax.legend(loc='lower left', fontsize=25, frameon=False)

plt.tight_layout()
out_path = 'injection_vs_equilibrium_losses.pdf'
plt.savefig(out_path, dpi=200, bbox_inches='tight')
