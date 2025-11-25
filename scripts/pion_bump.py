import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

# Neutral pion mass in GeV
m_pi = 0.135
E_mid = m_pi / 2.0  # ~ 67.5 MeV

def Emin_Emax_from_Epi(E_pi):
    """
    Given pion energy E_pi (in GeV), return the minimum and maximum
    gamma-ray energies (in GeV) from pi0 -> 2 gamma decay in the LAB frame.
    """
    gamma = E_pi / m_pi
    beta = np.sqrt(1.0 - 1.0 / gamma**2)
    Emin = 0.5 * m_pi * gamma * (1.0 - beta)
    Emax = 0.5 * m_pi * gamma * (1.0 + beta)
    return Emin, Emax

# Energy grid for gamma rays
E_gamma = np.logspace(-4, 2, 1000)  # 1 MeV to 100 GeV

# ---------------------------------------------------------------------
# 1) A few discrete pion energies to show individual "boxes"
# ---------------------------------------------------------------------
pion_energies_demo = [0.2, 0.5, 1.0, 2.0, 5.0]  # GeV
box_spectra_demo = []

for E_pi in pion_energies_demo:
    Emin, Emax = Emin_Emax_from_Epi(E_pi)
    y = np.zeros_like(E_gamma)

    # uniform in E between Emin and Emax (normalized to area=1)
    mask = (E_gamma >= Emin) & (E_gamma <= Emax)
    if Emin < Emax:
        y[mask] = 1.0 / (Emax - Emin)

    box_spectra_demo.append((E_pi, y, Emin, Emax))

# ---------------------------------------------------------------------
# 2) A more realistic superposition of many boxes to get a "pion bump"
# ---------------------------------------------------------------------
def total_gamma_spectrum(E_gamma, n_pions=5000):
    """
    Construct a toy total gamma-ray spectrum by superposing many
    box-like spectra from pi0 decay, assuming dN_pi/dE_pi ∝ E_pi^-2.
    """
    E_pi_array = np.logspace(np.log10(0.13), np.log10(1000.0), n_pions)  # GeV
    weights = E_pi_array**-2  # toy power-law distribution of pions

    total = np.zeros_like(E_gamma)

    for E_pi, w in zip(E_pi_array, weights):
        Emin, Emax = Emin_Emax_from_Epi(E_pi)
        if Emin >= Emax:
            continue
        mask = (E_gamma >= Emin) & (E_gamma <= Emax)
        # uniform box, weighted by pion spectrum
        total[mask] += w / (Emax - Emin)

    return total

# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.0))

colors = ['tab:olive', 'tab:orange', 'tab:green', 'tab:pink', 'tab:purple']

# Left panel: individual boxes for different E_pi
for i, (E_pi, y, Emin, Emax) in enumerate(box_spectra_demo):
    ax1.plot(E_gamma, y, label=fr"$E_\pi = {E_pi:.1f}\,\mathrm{{GeV}}$", color=colors[i])
    # optional: mark the edges
    ###ax1.axvline(Emin, linestyle=':', alpha=0.3)
    ###ax1.axvline(Emax, linestyle=':', alpha=0.3)

# vertical line at m_pi/2 (common log-midpoint of all boxes)
ax1.axvline(E_mid, linestyle='--', label=r"$m_\pi/2$", alpha=0.8, color='tab:gray')

ax1.set_xscale("log")
ax1.set_xlim([0.5e-3, 1e1])
ax1.set_ylim([5e-2, 1e1])
ax1.set_yscale("log")
ax1.set_xlabel(r"$E_\gamma\ \mathrm{[GeV]}$")
ax1.set_ylabel(r"$dN_\gamma/dE_\gamma$ (arb. units)")
#ax1.set_title("Box-like spectra from individual $\pi^0$ energies")
ax1.legend(fontsize=14, loc="upper left")

total_spec = total_gamma_spectrum(E_gamma)

for i, (E_pi, y, Emin, Emax) in enumerate(box_spectra_demo):
    y = 0. * E_gamma
    print (E_pi)
    w = E_pi**-2  # toy power-law distribution of pions
    mask = (E_gamma >= Emin) & (E_gamma <= Emax)
    y[mask] = w / (Emax - Emin)
    ax2.plot(E_gamma, 1e2 * E_gamma**2. * y, color=colors[i])
    
# Right panel: superposed boxes -> "pion bump" in E^2 dN/dE
ax2.loglog(E_gamma, E_gamma**2 * total_spec, color='darkblue', lw=5)
ax2.set_xlim([1e-3, 20])
ax2.set_ylim([1e-6, 1e4])
ax2.axvline(E_mid, linestyle='--', alpha=0.8, color='tab:gray')

ax2.set_xlabel(r"$E_\gamma\ \mathrm{[GeV]}$")
ax2.set_ylabel(r"$E_\gamma^2\,dN_\gamma/dE_\gamma$ (arb. units)")
#ax2.set_title(r"Superposition of boxes: pion bump")

plt.tight_layout()

out_path = "pion_bump.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=200)
