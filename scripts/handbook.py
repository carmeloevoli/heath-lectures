import numpy as np
import math

import constants

def chapter1():
    def tau_cooling():
        gamma_electron = constants.TeV / constants.electron_mass_c2
        U_B = constants.eV / constants.cm3
        tau = 3. / 4. * constants.electron_mass * constants.c_light / constants.sigma_T
        tau /= gamma_electron * U_B
        print(f'tau_cool : {tau/constants.Myr:3.0e} Myr')
    def critical_frequency():
        B = 1e-6 # Gauss
        gamma_electron = constants.GeV / constants.electron_mass_c2
        nu = 3. / 4. / math.pi * gamma_electron**2.0
        nu *= constants.elementary_charge * B / constants.electron_mass / constants.c_light
        print(f'nu_c : {nu/1e6:3.1f} Mhz')
    
    tau_cooling()
    critical_frequency()
    
# Chapter 3
def shockmfp():
    # Atmosphere
    n = 1e23 # cm-3
    r_A = 65e-10 # cm [Nitrogen covalent radius]
    sigma = math.pi * r_A**2.0
    mfp = 1. / n / sigma
    print(f'sigma : {sigma:3.0e} / mfp : {mfp:3.0e} cm')
    
    n = 1.
    r_0 = 1.2 * np.power(14., 1./3.) * 1e-13
    sigma = math.pi * r_0**2.0
    mfp = 1. / n / sigma
    print(f'sigma : {sigma:3.0e} / mfp : {mfp/constants.Mpc:3.0e} Mpc')

# Chapter 4
def Hillas():
    q = constants.elementary_charge
    L = constants.pc
    B = constants.muG
    u = 1e3 * constants.km / constants.sec
    c = constants.c_light
    
    Emax = q * L * B * u / c
    print(f'Emax : {Emax / constants.eV:3.1e} eV')

    Emax = 1e20 * constants.eV
    Wb = Emax * Emax * L / 6. / q / q
    print(f'Wb : {Wb / constants.erg:3.1e} erg')

def acceleration_time():
    D = 1e28 * constants.cm2 / constants.sec
    u = 1e4 * constants.km / constants.sec

    tau = 4. * D / u / u
    print(f'tau_acc : {tau / constants.kyr:3.1e} kyr')

# def taue_Be(Be10Be9):
#     gamma = 10.
#     tau_d = 1.36 / np.log(2.) * Myr
#     tau_e = gamma * tau_d / Be10Be9**2.
#     print ('tau_e : %5.1f Myr' % (tau_e / Myr))
    
# def taue_Be_LBM(Be10Be9):
#     gamma = 10.
#     tau_d = 1.36 / np.log(2.) * Myr
#     tau_e = gamma * tau_d / Be10Be9
#     print ('tau_e : %5.1f Myr' % (tau_e / Myr))

# def halo_size():
#     nd = 1. / cm**3.0
#     tau_e = 200. * Myr
#     chi = 8. * g / cm**2.
#     H = mp * nd * h * c * tau_e / chi
#     print ('H : %5.1f kpc' % (H / kpc))

if __name__== "__main__":
    chapter1()


