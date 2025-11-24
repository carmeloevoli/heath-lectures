import numpy as np
import math

# CGS UNITS
sec = 1.
cm = 1.
gr = 1.
erg = 1.
K = 1.
Coulomb = 1.
Gauss = 1.
sr = 1.

# DERIVED UNITS
sec2 = sec * sec
eV = 1. / 6.242e+11 * erg
GeV = 1e9 * eV
TeV = 1e12 * eV
PeV = 1e15 * eV
EeV = 1e18 * eV
muG = 1e-6 * Gauss
nG = 1e-9 * Gauss
cm2 = cm * cm
cm3 = cm * cm * cm
m = 1e2 * cm
m2 = m * m
km = 1e5 * cm
pc = 3.086e18 * cm
kpc = 1e3 * pc
Mpc = 1e6 * pc
Mpc3 = Mpc * Mpc * Mpc
year = 3.154e7 * sec
kyr = 1e3 * year
Myr = 1e6 * year
Gyr = 1e9 * year

# CONSTANTS
c_light = 2.998e10 * cm / sec
elementary_charge = 4.8032047e-10 * Coulomb
electron_radius = 2.8179e-13 * cm
electron_mass = 9.1093837015e-28 * gr
electron_mass_c2 = electron_mass * c_light * c_light
proton_mass = 1.67262192e-24 * gr
proton_mass_c2 = proton_mass * c_light * c_light
sun_mass = 1.989e33 * gr
k_B = 1.380649e-16 * erg / K
G_N = 6.67430e-8 * cm3 / gr / sec2
sigma_T = 6.6524587e-25 # cm2

# COSMOLOGICAL PARAMETERS
# T_IGM = 1e4 * K
# h_little = 0.7
# Omega_b = 0.048
# #H_0 = h_little * 100. * km / Mpc
# rho_critical = 1.88e-29 * np.power(h_little, 2.) * gr / cm3
# delta_vir = 1.

# CONSTANTS
#c_light = 2.998e10 # cm / s
#me_c2 = 0.5109989461e6 # eV
#U_CMB = 0.25 # eV / cm3
#E_CMB = 6e-4 # eV
#electron_radius = 2.8179e-13 # cm
#year = 3.154e7 # s
#km = 1e5
#pc = 3.086e18 # cm
#kpc = 1e3 * pc # cm
#Mpc = 1e6 * pc # cm
#Mpc3 = np.power(Mpc, 3.) # cm3
#erg2eV = 6.242e+11
#sigma_SB = 5.670374419e-5 * erg2eV # eV / cm2 / s / K^4
#k_B = 8.617333262e-5 # eV / K
#h_little = 0.7
#h_little2 = h_little * h_little
#H_0 = h_little * 100. * km / Mpc
#Omega_b = 0.048
#Omega_m = 0.3
#G = 6.67430e-8 # cm3 / g / s2
#proton_mass = 1.67262192e-24 # g
#sun_mass = 1.989e33 # g
#critical_density = 2.7754e11 * h_little2 * sun_mass / Mpc3 # g / cm3
