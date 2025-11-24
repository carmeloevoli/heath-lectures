# Retry: turbulence cascade schematic with spirals and right-side labels.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

def spiral(a, b, theta_max, n=400):
    th = np.linspace(0, theta_max, n)
    r = a + b*th
    x = r * np.cos(th)
    y = r * np.sin(th)
    return x, y

fig, ax = plt.subplots(figsize=(9, 5.2))

y_inj, y_mid, y_diss = 1.6, 0.5, -0.7
x_start, gap = -3.8, 1.9

# Row 1: large eddies (injection)
centers1 = [x_start + i*(gap*0.80) for i in range(7)]
for cx in centers1:
    x,y = spiral(0.012, 0.060, 4*np.pi)
    ax.plot(cx + x, y_inj + y, lw=2.5)

## Row 2: medium eddies (cascade)
centers2 = [x_start + i*(gap*0.55) for i in range(14)]
for cx in centers2:
    x,y = spiral(0.012, 0.035, 4*np.pi)
    ax.plot(cx + x, y_mid + y, lw=2.0)

## Row 3: small eddies
centers3 = [x_start + i*(gap*0.37) for i in range(21)]
for cx in centers3:
    x,y = spiral(0.012, 0.025, 4*np.pi)
    ax.plot(cx + x, y_diss + 0.35 + y*0.7, lw=1.6)

## Tiny-scale dots (dissipation tail)
#for i in range(55):
#    ax.plot([x_start + i*0.18 - 0.2], [y_diss - 0.05], marker='o', ms=1.5, lw=0)
#
## Right-side arrows and labels
#ax.annotate(r"$\varepsilon$", xy=(4.7, y_inj+0.6), xytext=(4.7, y_inj+0.25),
#            arrowprops=dict(arrowstyle="->", lw=2.5))
#ax.text(5.1, y_inj+0.25, "Energy injection", fontsize=12, va='center')
#
#ax.annotate(r"$\varepsilon$", xy=(4.7, y_mid+0.55), xytext=(4.7, y_mid+0.1),
#            arrowprops=dict(arrowstyle="->", lw=2.5))
#ax.text(5.1, y_mid+0.1, "Energy cascade", fontsize=12, va='center')
#
#ax.annotate(r"$\varepsilon$", xy=(4.7, y_diss+0.15), xytext=(4.7, y_diss-0.35),
#            arrowprops=dict(arrowstyle="->", lw=2.5))
#ax.text(5.1, y_diss-0.35, "Energy dissipation", fontsize=12, va='center')

ax.set_xlim(-4.5, 6.5)
ax.set_ylim(-1.5, 2.2)
ax.set_xticks([]); ax.set_yticks([])
ax.set_frame_on(False)

plt.tight_layout()
plt.savefig('turbulence_cascade_spirals.pdf', dpi=300, bbox_inches="tight")
    
