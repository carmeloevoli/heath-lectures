import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('review.mplstyle')
import numpy as np
import math

### UNITS
cm = 1.
sec = 1.
gr = 1.
erg = 1.
sr = 1.

meter = 1e2 * cm
m2 = meter * meter
year = 3.14e7 * sec
Myr = 1e6 * year
km = 1e5 * cm
parsec = 3.1e18 * cm
kpc = 1e3 * parsec
mbarn = 1e-27 * cm**2.0
eV = 1.60218e-12 * erg
MeV = 1e6 * eV
GeV = 1e9 * eV

### CONSTANTS
cLight = 3.00e10 * cm / sec
protonMass = 1.66e-24 * gr
protonMassC2 = 0.938 * GeV
electronMass = 9.11e-28 * gr
electronMassC2 = 0.511 * MeV
sigmaTh = 6.65e-25 * cm**2.0
sigmaPP = 3.00e-26 * cm**2.0
HeHism = 0.1
ndisk = 1. / cm**3.0
hdisk = 100. * parsec
H = 5. * kpc
Rdisk = 10. * kpc
SnRate = 1. / 100. / year
ESN = 1e51 * erg
mu_d = 2.3e-3 * gr / cm**2.0

def handbook():
    def tau_disk():
        chi_BC = 10. * gr / cm**2.0
        return chi_BC / mu_d * 2. * hdisk / cLight
    
    def n_mean():
        chi_BC = 10. * gr / cm**2.0
        tau_H = 6e7 * year
        return chi_BC / cLight / tau_H / (1.4 * protonMass)
        
    def tau_esc_naive():
        BC = 0.3
        H_here = 3. * kpc
        sigma_CB = 60. * mbarn
        return 2. * BC * (1.4 * protonMass) * H_here / cLight / mu_d / sigma_CB
        
    def H_from_grammage():
        tau_esc = 200. * Myr
        chi_BC = 10. * gr / cm**2.0
        return 0.5 * mu_d * cLight * tau_esc / chi_BC
    
    def losses_electron(E):
        gamma = E / electronMassC2
        U = eV / cm**3.0
        dEdt = 4./3. * cLight * sigmaTh * gamma**2.0 * U
        return dEdt
    
    def horizon_electron(E):
        tauLoss = E / losses_electron(E)
        tauEsc = 100. * Myr * (E / 10. / GeV)**(-0.4)
        return np.sqrt(tauLoss / tauEsc)
        
    def N(E):
        tauLoss = E / losses_electron(E)
        tauEsc = 100. * Myr * (E / 10. / GeV)**(-0.4)
        return SnRate / Rdisk**2.0 * H**2.0 * tauLoss**2.0 / tauEsc
        
    def Ip(E):
        L = 1e40 * erg / sec
        piRdmp2 = np.power(math.pi * Rdisk * protonMassC2, 2.)
        slope = 4.8
        tauEsc = 100. * Myr * (E / 10. / GeV)**(-0.4)
        Igamma = 2.5
        return L * cLight / 8. / piRdmp2 * np.power(E / GeV, 2. - slope) * tauEsc / H / Igamma
        
    E = 10. * GeV
    print (f'tau disc at 10 GeV : {tau_disk() / Myr:5.0f} Myr')
    print (f'tau ballistic : {(2. * hdisk / cLight) / year:5.1e} yr')
    print (f'tau esc naive : {tau_esc_naive() / Myr:5.1e} Myr')
    print (f'H from X : {H_from_grammage() / kpc:5.1e} kpc')
    print (f'n mean : {n_mean():5.1e} ')
    print (f'dEdt at 10 GeV : {losses_electron(E) / (GeV/sec):5.1e} GeV/s')
    print (f'tau loss at 10 GeV : {(E / losses_electron(E)) / Myr:5.0f} Myr')
    print (f'horizon at 10 GeV : {horizon_electron(E):5.2f}')
    print (f'Ip at 10 GeV : {E*E*Ip(E)/(GeV/m2/sec/sr):5.2e}')
    print (f'L_SN : {SnRate * ESN / (erg/sec):5.2e}')

    E = 1e3 * GeV
    print (f'N at 1 TeV : {N(E):5.2f}')

def plot_grammage_pillar():
    def set_axes(ax):
        ax.set_ylabel(r'secondary / primary')
        ax.set_ylim([0,0.6])
        ax.set_xlabel(r'grammage [g/cm$^2$]')
        ax.set_xlim([0,20])
        
    def lambda_A(A):
        mbarn = 1e-27 # cm2
        proton_mass = 1.6726219e-24 # g
        sigma = 45. * mbarn * np.power(A, 0.7) # cm2
        mass = 1.4 * proton_mass # g
        return mass / sigma
    
    def P_BC():
        mbarn = 1e-27 # cm2
        proton_mass = 1.6726219e-24 # g
        A = 12.0 # 0
        sigma = 45. * mbarn * np.power(A, 0.7) # cm2
        sigma_B = 15. + 25. + 25. # B10 + B11 + C11
        sigma_B *= mbarn
        return (sigma_B / sigma)
        
    def plot_model(ax, color, lambda_s, lambda_p, P):
        X = np.linspace(0, 20, 2000)
        r = P * lambda_s / (lambda_s - lambda_p) * (np.exp(-X / lambda_s + X / lambda_p) - 1.0)
        ax.plot(X, r, color=color, zorder=1, lw=5)

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    plot_model(ax, 'tab:orange', lambda_A(10.), lambda_A(12.), P_BC())
    
    print (f'lambda_B : {lambda_A(10.):5.1f}')
    print (f'lambda_C : {lambda_A(12.):5.1f}')
    print (f'P_BC : {P_BC():5.2f}')

    ax.hlines(0.286, 0, 100, linestyle='--', color='tab:blue', linewidth=5)
    ax.fill_between([0,100], 0.286 - 12e-03, 0.286 + 12e-03, color='tab:blue', alpha=0.15) # 2 sigmas
    
    ax.text(14.5, 0.24, 'B/C at 10 GV', color='tab:blue', fontsize=22)

    ax.text(1., 0.55, r'$\lambda_B = 10.4$ g/cm$^2$', fontsize=22)
    ax.text(1., 0.50, r'$\lambda_C = 9.1$ g/cm$^2$', fontsize=22)
    ax.text(1., 0.45, r'$P_{C \rightarrow B} = 0.25$', fontsize=22)
    
    ax.legend()
    plt.savefig('grammage_pillar.pdf')

def plot_diffusion_softening():
    def set_axes(ax):
        ax.set_ylabel(r'intensity')
        ax.set_ylim([1e-2,2])
        ax.set_yscale('log')
        ax.set_xlabel(r'energy')
        ax.set_xlim([1,1e3])
        ax.set_xscale('log')

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    T = np.logspace(0, 3, 100)

    ax.plot([10.,10.], [np.power(10. / T[0], -0.2), np.power(10. / T[0], -0.66)], color='tab:orange', linestyle=':', lw=2)
    ax.text(10., .80, 'slow escape', color='tab:orange', fontsize=18, ha='center', va='center')

    ax.plot([500.,500.], [np.power(500. / T[0], -0.2), np.power(500. / T[0], -0.66)], color='tab:orange', linestyle=':', lw=2)
    ax.text(500., .35, 'fast escape', color='tab:orange', fontsize=18, ha='center', va='center')

    ax.plot(T, np.power(T / T[0], -0.2), color='tab:red', label='injection')
    ax.plot(T, np.power(T / T[0], -0.66), color='tab:blue', label='after propagation')

    ax.text(70, 0.25, r'$E^{-\gamma}$', color='tab:red', fontsize=33)
    ax.text(70, 0.02, r'$E^{-\gamma-\delta}$', color='tab:blue', fontsize=33)
    
    ax.legend()
    plt.savefig('diffusion_softening.pdf')
    
def plot_critical_grammage():
    def set_axes(ax):
        ax.set_xscale('log')
        ax.set_xlim([1e1, 1e3])
        ax.set_yscale('log')
        ax.set_ylim([0.5, 10])
        ax.set_xlabel('R [GV]')
        ax.set_ylabel('$\chi$ [gr/cm$^2$]')
    
    def galactic_grammage(R):
        s = 0.1
        Delta_delta = 0.2
        u = 5.0 * km / sec
        delta = 0.54
        D_0 = 2.2 * 1e28 * cm**2. / sec
        H = 5. * kpc
        R_b = 312. * GeV
        mu = 2.3e-3 * gr / cm**2.
        D_R = D_0 * np.power(R / GeV, delta) / np.power(1. + np.power(R / R_b, Delta_delta / s), s)
        X = mu * (cLight / 2. / u) * (1. - np.exp(-u * H / D_R))
        return X
        
    def critical_grammage(A):
        Sigma_He = np.power(4., 2./3.)
        m = protonMass * (1. + Sigma_He * HeHism) / (1. + HeHism)
        sigma = 45. * np.power(A, 0.7) * mbarn
        return m / sigma

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)

    R = np.logspace(1, 3, 100) * GeV
    X = galactic_grammage(R)
    ax.plot(R / GeV, X, lw=5, color='tab:blue', label='this work')

    ax.hlines(critical_grammage(12.), 1, 1e4, linestyle='--', color='tab:green')
    ax.hlines(critical_grammage(16.), 1, 1e4, linestyle='--', color='tab:orange')
    ax.hlines(critical_grammage(56.), 1, 1e4, linestyle='--', color='tab:red')

    ax.text(400, 8.05, 'C$^{12}_{6}$', fontsize=19, color='tab:green')
    ax.text(400, 5.15, 'O$^{16}_{8}$', fontsize=19, color='tab:orange')
    ax.text(400, 2.75, 'Fe$^{56}_{26}$', fontsize=19, color='tab:red')
    ax.text(300, 0.84, 'Galactic', fontsize=22, color='tab:blue')

    plt.savefig('grammage_critical.pdf')
    
#def plot_data(ax, filename, slope, color, label, fmt, norm):
#    T, y, err_y_lo, err_y_up = np.loadtxt(filename, skiprows=7, usecols=(0,1,2,3), unpack=True)
#    y *= norm
#    err_y_lo *= norm
#    err_y_up *= norm
#    y_err = [np.power(T, slope) * err_y_lo, np.power(T, slope) * err_y_up]
#    y_plot = np.power(T, slope) * y
#    x_plot = T
#    ax.errorbar(x_plot, y_plot, yerr=y_err, label=label,
#                fmt=fmt, color=color, markeredgecolor=color,
#                markersize=7, elinewidth=2, capsize=4, capthick=2, zorder=1)

def plot_libeb_ams02():
    def set_axes(ax):
        ax.set_xscale('log')
        ax.set_xlim([1e1, 1e3])
        ax.set_xlabel('R [GV]')
        ax.set_ylabel('secondary/primary')
        ax.set_ylim([0.05,0.3])

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    Xcr = protonMass / 60. / mbarn
    p = np.logspace(1, 3, 100)
    X = (8.5 / Xcr) * (p / p[0])**(-0.36)
    ax.plot(p, X, '--', color='tab:gray', zorder=1, lw=3, label=r'$\chi = 8.5$~g cm$^{-2}$ (R / 10 GV)$^{-0.36}$')

    plot_data(ax, 'AMS-02_Be_C_rigidity.txt', 0., 'tab:orange', 'Be/C (x 2.7)', 'o', 2.7)
    plot_data(ax, 'AMS-02_Li_C_rigidity.txt', 0., 'tab:blue', 'Li/C (x 1.4)', 'o', 1.4)
    plot_data(ax, 'AMS-02_B_C_rigidity.txt', 0., 'tab:red', 'B/C', 'o', 1)

    ax.text(14., 0.07, 'data from AMS-02', fontsize=20)

    ax.legend(fontsize=22)
    plt.savefig('LiBeB_C_AMS02.pdf')

def plot_protons_he():
    def set_axes(ax):
        ax.set_xscale('log')
        ax.set_xlim([1e1, 2e3])
        ax.set_xlabel('R [GV]', labelpad=10)
        #ax.set_yscale('log')
        ax.set_ylim([1.4, 2.2])
        ax.set_ylabel(r'$R^{2.8}$ I$_{\rm H}$', labelpad=10)

    fig = plt.figure(figsize=(11.5, 8))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    plot_data(ax, 'PAMELA_H_rigidity.txt', 2.8, 'tab:orange', 'PAMELA', 'o', 0.93e-4)
    plot_data(ax, 'AMS-02_H_rigidity.txt', 2.8, 'tab:blue', 'AMS-02', 'o', 1e-4)

    ax.legend()
    ax.text(13, 1.45, '10$^{-4}$ GV$^{-1}$ m$^{-2}$ s$^{-1}$ sr$^{-1}$', fontsize=20)

    plt.savefig('protons_he.pdf',format='pdf',dpi=300)

def plot_pamelamodulated_data(ax, filename, slope, color, norm):
    filename = 'pamela/' + filename
    T, y, err_y_lo, err_y_up = np.loadtxt(filename, skiprows=3, usecols=(1,4,9,10), unpack=True)
    y *= norm
    err_y_lo *= norm
    err_y_up *= norm
    y_err = [np.power(T, slope) * err_y_lo, np.power(T, slope) * err_y_up]
    y_plot = np.power(T, slope) * y
    x_plot = T
    sort = np.argsort(x_plot)
    return x_plot[sort], y_plot[sort]

def plot_protons_le():
    def set_axes(ax):
        ax.set_xscale('log')
        ax.set_xlim([1e-1, 60.])
        ax.set_xlabel('T [GeV]', labelpad=10)
        #ax.set_yscale('log')
        ax.set_ylim([0, 3000])
        ax.set_ylabel(r'$E^{2}$ I$_{\rm H}$ [GeV m$^{-2}$ s$^{-1}$ sr$^{-1}$]', labelpad=10)

    fig = plt.figure(figsize=(11.5, 8))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    x = []
    y_min = np.zeros(78) + 1e10
    y_max = np.zeros(78)
    
    for i in range(1,78):
        x, y = plot_crdb_data(ax, 'data_exp' + str(i) + '.dat', 2., 'tab:blue', 1.)
        #ax.plot(x, y, 'o', color='tab:gray')
        for j in range(78):
            y_min[j] = min(y_min[j], y[j])
            y_max[j] = max(y_max[j], y[j])

    ax.fill_between(x, y_min, y_max, color='tab:orange', alpha=0.5)
    ax.vlines(10., 0., 3000., linestyle=':', color='k')
    
    ax.text(0.15, 2600., 'PAMELA [2006/07-2014/02]', fontsize=22)

    plt.savefig('protons_le.pdf',format='pdf',dpi=300)

def plot_beb_ams02():
    def set_axes(ax):
        ax.set_xlim([2e0,1e3])
        ax.set_xscale('log')
        ax.set_ylim([0.2,0.5])
        ax.set_xlabel('R [GV]', labelpad=10)
        ax.set_ylabel(r'Be/B', labelpad=10)

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    plot_data(ax, 'AMS-02_Be_B_rigidity.txt', 0., 'tab:red', 'Be/O', 'o', 1)
    ax.hlines(0.36, 1e0, 1e3, linestyle='--', color='tab:gray', zorder=1)

    plt.savefig('BeB_AMS02.pdf')
    
def plot_crdb_data(ax, filename, slope, color, label, fmt, norm):
    filename = 'crdb/' + filename
    T, y, err_y_lo, err_y_up = np.loadtxt(filename, skiprows=3, usecols=(1,4,9,10), unpack=True)
    y *= norm
    err_y_lo *= norm
    err_y_up *= norm
    y_err = [np.power(T, slope) * err_y_lo, np.power(T, slope) * err_y_up]
    y_plot = np.power(T, slope) * y
    x_plot = T
    ax.errorbar(x_plot, y_plot, yerr=y_err, label=label,
        fmt=fmt, color=color, markeredgecolor=color,
        markersize=7, elinewidth=2, capsize=4, capthick=2, zorder=1)

def plot_bc_he():
    def set_axes(ax):
        ax.set_xlim([1e1,6e3])
        ax.set_xscale('log')
        ax.set_ylim([0.01,0.3])
        ax.set_xlabel('E [GeV/n]', labelpad=10)
        ax.set_yscale('log')
        ax.set_ylabel(r'B/C', labelpad=10)

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    plot_crdb_data(ax, 'AMS-02_BC_Ekn.txt', 0., 'tab:orange', 'AMS-02', 'o', 1)
    plot_crdb_data(ax, 'DAMPE_BC_Ekn.txt', 0., 'tab:red', 'DAMPE', 'o', 1)
    plot_crdb_data (ax, 'CALET_BC_Ekn.txt', 0., 'tab:purple', 'CALET', 'o', 1)

    E = np.logspace(1, 4, 100)
    BC = 0.21 * (E / E[0])**(-0.36)

    ax.plot(E, BC, ':', color='tab:gray')

    ax.legend()
    plt.savefig('BC_highenergy.pdf')

def plot_electron_losses():
    def set_axis(ax):
        ax.set_xscale('log')
        ax.set_xlabel('E [GeV]')
        ax.set_xlim([1e0, 1e3])
        ax.set_yscale('log')
        ax.set_ylabel(r'$\tau$ [Myr]')
        ax.set_ylim([0.1, 3e3])

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axis(ax)
    
    E = np.logspace(0, 4, 100)
    tauLosses = 30. * Myr / (E / 10.)
    tauIn = 1. / (cLight * sigmaPP * ndisk * (hdisk / H))
    tauEsc = 100. * Myr * (E / 10.)**(-0.4)
    
    ax.fill_between(E, tauEsc / Myr, 1e4, color='tab:blue', alpha=0.2)
    ax.plot(E, tauEsc / Myr, color='tab:blue', linestyle='-', label=r'escape $H^2/D$')
    ax.plot(E, tauLosses / Myr, color='tab:red', linestyle='-', label=r'leptonic losses $E/\dot E$')
    ax.hlines(tauIn / Myr, 1e0, 1e4, color='tab:olive', linestyle='--', label=r'proton lossses $1 / (c \bar n \sigma_{pp})$')

    ax.legend(fontsize=20, loc='lower left')
    plt.savefig('electron_losses.pdf')
    
def plot_H_electron_ratio():
    def set_axis(ax):
        ax.set_xscale('log')
        ax.set_xlabel('R [GV]')
        ax.set_xlim([1e1, 1e3])
        ax.set_yscale('log')
        ax.set_ylabel(r'H/leptons')
        ax.set_ylim([1., 10.])

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axis(ax)
    
    plot_data(ax, 'AMS-02_H_e+_rigidity.txt', 0., 'tab:purple', 'H/$e^+$ [10$^{-3}$]', 'o', 1e-3)
    plot_data(ax, 'AMS-02_H_e-_rigidity.txt', 0., 'tab:red', 'H/$e^-$ [10$^{-2}$]', 'o', 1e-2)

    E = np.logspace(1,3,100)
    ax.plot(E, 1.45 * (E / E[0])**0.37, linestyle='--', color='tab:gray', label='E$^{0.4}$')

    ax.legend()
    plt.savefig('H_electron_ratio.pdf')

def plot_positron_fraction():
    def set_axis(ax):
        ax.set_xscale('log')
        ax.set_xlabel('E [GeV]')
        #ax.set_xlim([1e1, 1e3])
        #ax.set_yscale('log')
        ax.set_ylabel(r'$e^+$/$e^+ + e^-$')
        ax.set_ylim([0., 0.25])

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axis(ax)
    
    plot_data(ax, 'FERMI_posfraction_kineticEnergy.txt', 0., 'tab:olive', 'Fermi-LAT', 'o', 1.)
    plot_data(ax, 'PAMELA_posfraction_kineticEnergy.txt', 0., 'tab:blue', 'PAMELA', 'o', 1.)
    plot_data(ax, 'AMS-02_posfraction_kineticEnergy.txt', 0., 'tab:red', 'AMS-02', 'o', 1.)

    ax.legend()
    plt.savefig('positron_fraction.pdf')

def plot_positron_production():
    from scipy.signal import savgol_filter

    def set_axes(ax):
        ax.set_xscale('log')
        ax.set_xlim([1e1, 1e3])
        ax.set_xlabel('E [GeV]')
        #ax.set_yscale('log')
        ax.set_ylabel('positron production ratio')
        ax.set_ylim([1., 2.])

    fig = plt.figure(figsize=(11.5, 8.5))
    ax = fig.add_subplot(111)
    set_axes(ax)
    
    filename = 'Orusa2022_pos_source.txt'
    E, qtrue, qnaive = np.loadtxt(filename, usecols=(0,3,4), unpack=True, skiprows=1)
    y = savgol_filter(qtrue / qnaive, 11, 3, mode='nearest') # window size 51, polynomial order 3
    ax.plot(E, y, label='Orusa+2022')

    filename = 'AAFRAG_pos_source.txt'
    E, qtrue, qnaive = np.loadtxt(filename, usecols=(0,3,4), unpack=True, skiprows=1)
    ax.plot(E, qtrue / qnaive, label='AAFrag(v101)')

    #ax.plot(E, qnaive, label='boh')

    ax.legend(fontsize=22)
    plt.savefig('positron_source_term.pdf')

if __name__== "__main__":
#    handbook()
#    plot_grammage_pillar()
#    plot_diffusion_softening()
#    plot_critical_grammage()
#    plot_libeb_ams02()
#    plot_protons_he()
#    plot_protons_le()
#    plot_beb_ams02()
#    plot_electron_losses()
#    plot_H_electron_ratio()
#    plot_positron_fraction()
#    plot_positron_production()
#    plot_bc_he()
    plot_pion_production()
