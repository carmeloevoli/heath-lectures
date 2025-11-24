# Retry: Kolmogorov turbulence cascade schematic with injection, inertial, and dissipation scales.
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

# Set up figure
fig = plt.figure(figsize=(15.5, 7.5))
ax = fig.add_subplot(111)

# Axes limits
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(-0.9, 0.9)

# Draw background magnetic field B0 as a thick arrow along +x
ax.annotate("", xy=(8, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->, head_width=0.55", lw=2.5))
ax.text(7.4, 0.03, r"$\mathbf{B}_0$", fontsize=28, ha="left", va="bottom")

# Draw a small sinusoidal transverse displacement envelope to suggest the wave pattern (schematic)
x = np.linspace(0, 8, 500)
y = 0.4*np.sin(2*np.pi*(x/2.0))  # wavelength ~ 2 units
ax.plot(x, y, lw=4.5, color='r')

# Draw delta v (transverse) at that point (upwards)
x0 = 3.0
y0 = 0.4*np.sin(2*np.pi*(x0/2.0))
ax.annotate("", xy=(x0, y0+0.5), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", lw=2))
ax.text(x0-0.06, y0+0.60, r"$\delta\mathbf{v},\delta\mathbf{B}\,\perp\,\mathbf{B}_0$", fontsize=24, ha="center", va="center")
ax.text(x0-0.06, y0+0.75, r"Transverse perturbation", fontsize=18, ha="center", va="center")

# Draw k (chosen parallel to B0 for a shear Alfvén wave)
ax.annotate("", xy=(7.0, 0.46), xytext=(6.0, 0.46), arrowprops=dict(arrowstyle="->", lw=2))
ax.text(x0+3.55, y0+0.60, r"$\mathbf{k}=k_\parallel\,\hat{\mathbf{b}}_0$", fontsize=24, ha="center", va="center")
ax.text(x0+3.55, y0+0.75, r"Propagation along $\mathbf{B}_0$", fontsize=18, ha="center", va="center")

# Wavelength marker along B0
lam_start, lam_end = 2.0, 4.0
ax.annotate("", xy=(lam_end, -0.6), xytext=(lam_start, -0.6), arrowprops=dict(arrowstyle="<->", lw=3.3, color='b'))
ax.text((lam_start+lam_end)/2, -0.75, r"$\lambda=\frac{2\pi}{k_\parallel}$", fontsize=25, ha="center", color='b')

# Clean up plot appearance
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

# Tight layout and save
plt.tight_layout()
plt.savefig('alfven_diagram.pdf', dpi=200, bbox_inches="tight")
