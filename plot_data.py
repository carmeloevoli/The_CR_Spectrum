import numpy as np

def errorbar(ax, x, y, yerr, color):
    ax.errorbar(x, y, yerr=yerr, fmt='o', markeredgecolor=color, color=color,elinewidth=2, capthick=2)

def TA_allparticle(ax, color, label):
    """
    TA all-particle spectrum
    column 1: log10(E/eV)
    column 2: E^3*J in [eV^2 km^-2 yr^-1 sr^-1]
    column 3: Err_low
    column 4: Err_up
    reference: Telescope Array Collaboration, PoS ICRC2017 (2018) 1096
    url: https://pos.sissa.it/301/1096
    note: the table has been provided by Armando di Matteo
    """
    filename = 'data/TA-ICRC2017.txt'
    log10E, E3J, Err_low, Err_up = np.loadtxt(filename, skiprows=5, usecols=(0,1,2,3), unpack=True)
    E = np.power(10., log10E) # eV
    x = E / 1e9 # GeV
    y = E3J / E / 3.15e22
    y_err_low = Err_low / E / 3.15e22
    y_err_up = Err_up / E / 3.15e22
    y_err = [y_err_low, y_err_up]
    errorbar(ax, x, y, y_err, color)
    print ("... plotted TA data between %6.2e and %6.2e GeV" % (min(x), max(x)))

def AUGER_allparticle(ax, color, label):
    """
    AUGER all-particle spectrum
    column 1: log10(E/eV)
    column 2: E*J in [m^-2 s^-1 sr^-1]
    column 3: Err_up
    column 4: Err_low
    reference: Pierre Auger collaboration, PoS ICRC2019 (2019) 450
    url: https://pos.sissa.it/358/450
    note: data downloaded from https://www.auger.org/index.php/science/data
    """
    filename = 'data/Auger2019.txt'
    log10E, EJ, Err_up, Err_low = np.loadtxt(filename, skiprows=5, usecols=(0,1,2,3), unpack=True)
    x = np.power(10., log10E) / 1e9
    y = EJ * np.power(10., log10E - 9.)
    y_err_lo = Err_low * np.power(10., log10E - 9.)
    y_err_up = Err_up * np.power(10., log10E - 9.)
    y_err = [y_err_lo, y_err_up]
    errorbar(ax, x, y, y_err, color)
    print ("... plotted AUGER data between %6.2e and %6.2e GeV" % (min(x), max(x)))
    
def ICETOP_allparticle(ax, color, label):
    """
    ICETOP all-particle spectrum
    column 1: E in [1e6 GeV]
    column 2: Flux in [GeV-1 m-2 s-1 sr-1]
    column 3: stat
    column 4: syst
    reference: Abbasi et al., Astroparticle Physics (2013) 44
    url: https://doi.org/10.1016/j.astropartphys.2013.01.016
    note: I ignore the systematic errors due to composition
    """
    filename = 'data/IceTop12.txt'
    E, J, stat, syst = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3), unpack=True)
    E *= 1e6
    x, y = E, E * E * J
    y_err = E * E * np.sqrt(stat * stat + syst * syst)
    errorbar(ax, x, y, y_err, color)
    print ("... plotted ICETOP data between %6.2e and %6.2e GeV" % (min(x), max(x)))

def KASCADEGrande_allparticle(ax, color, label):
    """
    KASCADE-Grande all-particle spectrum
    column 1: E in [GeV]
    column 2: dJdE in [m-2 sr-1 s-1 GeV-1]
    column 3: stat
    column 4: syst
    reference: Apel et al., Astroparticle Physics (2013) 47
    url: https://doi.org/10.1016/j.astropartphys.2013.06.004
    """
    filename = 'data/KascadeGrande2013.txt'
    E, J, stat, syst = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3), unpack=True)
    x, y = E, E * E * J
    y_err = E * E * np.sqrt(stat * stat + syst * syst)
    errorbar(ax, x, y, y_err, color)
    print ("... plotted KASCADE-Grande data between %6.2e and %6.2e GeV" % (min(x), max(x)))

def Tibet_allparticle(ax, color, label):
    """
    Tibet all-particle spectrum
    column 1: E in [GeV]
    column 2: dJdE in [m􏰁-2 s-􏰁1 sr-􏰁1 GeV-􏰁1]
    column 3: stat errors
    reference: Amenomori et al., The Astrophysical Journal (2008) 678
    url:
    note: I am using the column of QGSJET+HD from Table 4 (syst errors?)
    """
    filename = 'data/Tibet-III.txt'
    E, y, err = np.loadtxt(filename,skiprows=1,usecols=(0,1,2),unpack=True)
    x, y = E, E * E * y
    y_err = E * E * err
    errorbar(ax, x, y, y_err, color)
    print ("... plotted Tibet data between %6.2e and %6.2e GeV" % (min(x), max(x)))

def HAWC_allparticle(ax, color, label):
    """
    HAWC all-particle spectrum
    column 1: log(E/GeV)
    column 2: dJdE in [GeV-1 s-1 m-2 sr−1]
    column 3: stat (symmetric)
    column 4: sys_MC (symmetric)
    column 5: sys up
    column 6: sys down
    reference: HAWC collaboration, Phys.Rev.D (2017) 96
    url: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.96.122001
    """
    filename = 'data/HAWC.txt'
    logE_min, logE_max, y, stat, sys_mc, sys_up, sys_do = np.loadtxt(filename,skiprows=1,usecols=(0,1,2,3,4,5,6),unpack=True)
    E_min = np.power(10., logE_min)
    E_max = np.power(10., logE_max)
    x = np.sqrt(E_min * E_max)
    y = x**2. * y
    err_y_lo = x**2. * (sys_mc + sys_do)
    err_y_hi = x**2. * (sys_mc + sys_up)
    y_err = [err_y_lo, err_y_hi]
    errorbar(ax, x, y, y_err, color)
    print ("... plotted HAWC data between %6.2e and %6.2e GeV" % (min(x), max(x)))

def FERMI_IGRB_gamma(ax, color, label):
    filename = 'data/EGB_Fermi.txt'
    E_min, E_max, f_igrb, errh_igrb, errl_igrb = np.loadtxt(filename, skiprows=24, usecols=(0,1,2,3,4), unpack=True)
    E = np.sqrt(E_min * E_max) / 1e3 # GeV
    x, y = E, E * f_igrb * 1e4
    y_err = E * errh_igrb * 1e4
    ax.errorbar(x, y, yerr=y_err, fmt='o', markeredgecolor=color, color=color,elinewidth=2, capthick=2, mfc='white')

def FERMI_diffuse_gamma(ax, color, label):
    E_1, f_1 = np.loadtxt('data/FERMI_DIFFUSE_1.txt', skiprows=0, usecols=(0,1), unpack=True)
    E_2, f_2 = np.loadtxt('data/FERMI_DIFFUSE_2.txt', skiprows=0, usecols=(0,1), unpack=True)
    E_3, f_3 = np.loadtxt('data/FERMI_DIFFUSE_3.txt', skiprows=0, usecols=(0,1), unpack=True)
    x = (np.array(E_1) + np.array(E_2) + np.array(E_3)) / 3.
    y = np.array(f_1) + np.array(f_2) + np.array(f_3)
    ax.plot(x / 1e3, y * 1e4 / 1e3, 'o', mfc='white', markersize=7, markeredgecolor=color, markeredgewidth=1.4, color=color)

#def AMS02_positrons(ax, color, label):
    
