import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

# Planck constant in eV*s
h_eVs = 4.135667696e-15

# Frequency range
nu_min, nu_max = 1e4, 1e25

fig, ax = plt.subplots(figsize=(18, 7))

ax.set_xscale('log')
ax.set_xlim(nu_min, nu_max)
ax.set_ylim(0, 1)
ax.set_yticks([])

ax.set_xlabel(r"Frequency $\nu$ [Hz]", fontsize=24)

ax.set_xticks([1e4, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16, 1e18, 1e20, 1e22, 1e24])

# Bands: (label, nu_low, nu_high)
bands = [
    ("Radio", 1e4, 3e8),
    ("Microwaves", 3e8, 3e11),
    ("Infrared (IR)", 3e11, 4e14),
    ("Optical (visible)", 4e14, 7.5e14),
    ("Ultraviolet (UV)", 7.5e14, 3e16),
    ("X-rays", 3e16, 3e19),
    ("Gamma rays", 3e19, 1e25),
]

for label, nu1, nu2 in bands:
    # Draw band edges
    ax.vlines([nu1, nu2], 0.1, 0.9, linestyles='dotted', linewidth=2)
    # Label in the middle (geometric mean)
    nu_c = np.sqrt(nu1 * nu2)
    ax.text(nu_c, 0.5, label, ha='center', va='center', rotation=90, fontsize=19)

# Secondary x-axis: photon energy
def nu_to_EeV(nu):
    return h_eVs * nu

def EeV_to_nu(E):
    return E / h_eVs

secax = ax.secondary_xaxis('top', functions=(nu_to_EeV, EeV_to_nu))
secax.set_xscale('log')
secax.set_xlabel(r"Photon energy $E_\gamma$ [eV]", fontsize=24)

secax.set_xticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0, 1e2, 1e4, 1e6, 1e8, 1e10])

#ax.set_title("Electromagnetic spectrum: frequency bands")

plt.tight_layout()

pdf_path = "em_spectrum_bands.pdf"
plt.savefig(pdf_path)
plt.close(fig)
