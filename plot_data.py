import numpy as np
from xml.dom import minidom
from scipy.interpolate import interp1d

def errorbar(ax, E, dJdE, dJdE_err, slope, color):
    x = np.copy(E)
    y = np.power(E, float(slope)) * dJdE
    yerr = np.power(E, float(slope)) * dJdE_err
    ax.errorbar(x, y, yerr=yerr, fmt='o', markeredgecolor=color, color=color, elinewidth=2, capthick=2)

def errorbar_H(ax, E, dJdE, dJdE_err, slope, color):
    x = np.copy(E)
    y = np.power(E, float(slope)) * dJdE
    yerr = np.power(E, float(slope)) * dJdE_err
    ax.errorbar(x, y, yerr=yerr, fmt='*', markeredgecolor=color, color=color, elinewidth=1, capthick=1)

def get_value(item, name):
    elem = item.getElementsByTagName(name)[0]
    return float(elem.firstChild.data)

def get_column_from_xml(item_name, ssdc_filename):
    tree = minidom.parse(ssdc_filename)
    items = tree.getElementsByTagName('DATA')
    v = []
    counter = 0
    for item in items:
        value = get_value(item, item_name)
        v.append(value)
        counter += 1
    return np.array(v)
    
def read_ssdc(xml_filename):
    E_min = get_column_from_xml('kinetic_energy_min', xml_filename)
    E_max = get_column_from_xml('kinetic_energy_max', xml_filename)
    E = np.sqrt(E_min * E_max)
    flux = get_column_from_xml('flux', xml_filename)
    stat_low = get_column_from_xml('flux_statistical_error_low', xml_filename)
    stat_high = get_column_from_xml('flux_statistical_error_high', xml_filename)
    sys_low = get_column_from_xml('flux_systematical_error_low', xml_filename)
    sys_high = get_column_from_xml('flux_systematical_error_high', xml_filename)
    err_low = np.sqrt(stat_low**2. + sys_low**2.)
    err_high = np.sqrt(stat_high**2. + sys_high**2.)
    return E, flux, err_low, err_high

def all_TA(ax, slope, color, label):
    """
    TA all-particle spectrum
    column 1: log10(E/eV)
    column 2: E^3*J in [eV^2 km^-2 yr^-1 sr^-1]
    column 3: Err_low
    column 4: Err_up
    reference: Telescope Array Collaboration, PoS ICRC2017 (2018) 1096
    url: https://pos.sissa.it/301/1096
    note: the file has been provided by Armando di Matteo
    """
    filename = 'data/all_TA2017.txt'
    log10E, E3J, Err_low, Err_up = np.loadtxt(filename, skiprows=5, usecols=(0,1,2,3), unpack=True)
    E = np.power(10., log10E) # eV
    E /= 1e9 # GeV
    dJdE = E3J / np.power(10., 3. * log10E) # eV^-1 km^-2 yr^-1 sr^-1
    dJdE /= 3.15e4 # GeV^-1 m^-2 s^-1 sr^-1
    dJdE_err_low = Err_low / np.power(10., 3. * log10E)
    dJdE_err_low /= 3.15e4
    dJdE_err_up = Err_up / np.power(10., 3. * log10E)
    dJdE_err_up /= 3.15e4
    dJdE_err = [dJdE_err_low, dJdE_err_up]
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted TA all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def all_AUGER(ax, slope, color, label):
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
    filename = 'data/all_Auger2019.txt'
    log10E, EJ, Err_up, Err_low = np.loadtxt(filename, skiprows=5, usecols=(0,1,2,3), unpack=True)
    E = np.power(10., log10E) # eV
    E /= 1e9 # GeV
    dJdE = EJ / E # GeV^-1 m^-2 s^-1 sr^-1
    dJdE_err_lo = Err_low / E
    dJdE_err_up = Err_up / E
    dJdE_err = [dJdE_err_lo, dJdE_err_up]
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted AUGER all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))
    
def all_ICETOP(ax, slope, color, label):
    """
    ICETOP all-particle spectrum
    column 1: log10(E/GeV)
    column 2: Flux in [GeV-1 m-2 s-1 sr-1]
    column 3: stat
    column 4: syst_down
    column 5: syst_up
    reference: Aartsen et al., Phys.Rev.D (2019) 100
    url: https://doi.org/10.1103/PhysRevD.100.082002
    note: Table III
    """
    filename = 'data/all_IceTop2019.txt'
    log10E, dJdE, stat, syst_do, syst_up = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    E = np.power(10., log10E)
    dJdE_err_lo = np.sqrt(stat * stat + syst_do * syst_do)
    dJdE_err_up = np.sqrt(stat * stat + syst_up * syst_up)
    dJdE_err = [dJdE_err_lo, dJdE_err_up]
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted ICETOP all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def all_ICETOP_ICECUBE(ax, slope, color, label):
    """
    ICETOP-ICECUBE coincidence analysis of all-particle spectrum
    column 1: log10(E/GeV)
    column 2: Flux in [GeV-1 m-2 s-1 sr-1]
    column 3: stat
    column 4: syst_down
    column 5: syst_up
    reference: Aartsen et al., Phys.Rev.D (2019) 100
    url: https://doi.org/10.1103/PhysRevD.100.082002
    note: Table IV
    """
    filename = 'data/all_IceTop-IceCube2019.txt'
    log10E, dJdE, stat, syst_do, syst_up = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    E = np.power(10., log10E)
    dJdE_err_lo = np.sqrt(stat * stat + syst_do * syst_do)
    dJdE_err_up = np.sqrt(stat * stat + syst_up * syst_up)
    dJdE_err = [dJdE_err_lo, dJdE_err_up]
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted ICETOP-ICECUBE all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def all_Tibet(ax, slope, color, label):
    """
    Tibet all-particle spectrum
    column 1: E in [GeV]
    column 2: dJdE in [m􏰁-2 s-􏰁1 sr-􏰁1 GeV-􏰁1]
    column 3: stat errors
    reference: Amenomori et al., The Astrophysical Journal (2008) 678
    url: https://iopscience.iop.org/article/10.1086/529514
    note: I am using the column of QGSJET+HD from Table 4
    """
    filename = 'data/all_Tibet2008.txt'
    E, dJdE, dJdE_err = np.loadtxt(filename,skiprows=1,usecols=(0,1,2),unpack=True)
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted Tibet all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def all_HAWC(ax, slope, color, label):
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
    note: from TABLE IV
    """
    filename = 'data/all_HAWC2017.txt'
    logE_min, logE_max, dJdE, stat, sys_mc, sys_up, sys_do = np.loadtxt(filename,skiprows=1,usecols=(0,1,2,3,4,5,6),unpack=True)
    E_min = np.power(10., logE_min)
    E_max = np.power(10., logE_max)
    E = np.sqrt(E_min * E_max)
    dJdE_err_lo = (sys_mc + sys_do)
    dJdE_err_up = (sys_mc + sys_up)
    dJdE_err = [dJdE_err_lo, dJdE_err_up]
    errorbar(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted HAWC all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def all_KASCADEGrande(ax, slope, color, label):
    """
    KASCADE-Grande all-particle spectrum
    column 1: E in [eV]
    column 2: dJdE in [m-2 sr-1 s-1 GeV-1]
    column 3: UncertLow
    column 4: UncertHigh
    reference: Arteaga-Velázquez et al., ICRC (2017) 316
    url: https://pos.sissa.it/301/316
    note: from https://kcdc.ikp.kit.edu - model KG_SIBYLL-23_all
    """
    filename = 'data/all_KASCADE-Grande2017.txt'
    E, dJdE, err_lo, err_up = np.loadtxt(filename, skiprows=2, usecols=(0,1,2,3), unpack=True)
    E /= 1e9 # GeV
    dJdE *= 1e9 # GeV^-1
    err_lo *= 1e9
    err_up *= 1e9
    errorbar(ax, E, dJdE, [err_lo, err_up], slope, color)
    print ("... plotted KASCADE-Grande all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def read_CREAM_flux(filename, A):
    T_min = get_column_from_xml('kinetic_energy_min', filename)
    T_max = get_column_from_xml('kinetic_energy_max', filename)
    T = np.sqrt(T_min * T_max)
    dJdT = get_column_from_xml('flux', filename)
    return T * A, dJdT / A

def all_CREAM(ax, slope, color, label):
    """
    """
    H_filename = 'data/p_flux_CREAMIII_ApJ2017_000.xml'
    T, dJdT = read_CREAM_flux(H_filename, 1.)
    log_H = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T, max_T = min(T), max(T)
    
    He_filename = 'data/He_flux_CREAMIII_ApJ2017_000.xml'
    T, dJdT = read_CREAM_flux(He_filename, 4.)
    log_He = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))
    
    C_filename = 'data/C_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(C_filename, 12.)
    log_C = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    O_filename = 'data/O_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(O_filename, 16.)
    log_O = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    Ne_filename = 'data/Ne_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(Ne_filename, 20.)
    log_Ne = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    Mg_filename = 'data/Mg_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(Ne_filename, 24.)
    log_Mg = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    Si_filename = 'data/Si_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(Si_filename, 28.)
    log_Si = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    Fe_filename = 'data/Fe_CREAMII_ApJ2009_000.xml'
    T, dJdT = read_CREAM_flux(Fe_filename, 56.)
    log_Fe = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    E = np.logspace(np.log10(min_T), np.log10(max_T), 100)
    dJdE = 0. * E
    for i in range(len(E)):
        E_i = E[i]
        dJdE[i] += np.power(10., log_H(np.log10(E_i)))
        dJdE[i] += np.power(10., log_He(np.log10(E_i)))
        dJdE[i] += np.power(10., log_C(np.log10(E_i)))
        dJdE[i] += np.power(10., log_O(np.log10(E_i)))
        dJdE[i] += np.power(10., log_Ne(np.log10(E_i)))
        dJdE[i] += np.power(10., log_Mg(np.log10(E_i)))
        dJdE[i] += np.power(10., log_Si(np.log10(E_i)))
        dJdE[i] += np.power(10., log_Fe(np.log10(E_i)))

    ax.plot(E, np.power(E, slope) * dJdE, color=color)

    print ("... plotted CREAM all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def read_AMS_flux(filename, A):
    T = get_column_from_xml('kinetic_energy', filename)
    dJdT = get_column_from_xml('flux', filename)
    return T * A, dJdT / A

def all_AMS(ax, slope, color, label):
    """
    """
    H_filename = 'data/p_AMS_PRL2015_ekin_000.xml'
    T, dJdT = read_AMS_flux(H_filename, 1.)
    log_H = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T, max_T = min(T), max(T)

    He_filename = 'data/He_AMS_PRL2017_ekin_000.xml'
    T, dJdT = read_AMS_flux(He_filename, 4.)
    log_He = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    C_filename = 'data/C_AMS_PRL2017_ekin_000.xml'
    T, dJdT = read_AMS_flux(C_filename, 12.)
    log_C = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    O_filename = 'data/O_AMS_PRL2017_ekin_000.xml'
    T, dJdT = read_AMS_flux(O_filename, 16.)
    log_O = interp1d(np.log10(T), np.log10(dJdT), kind='cubic')
    min_T = max(min_T, min(T))
    max_T = min(max_T, max(T))

    E = np.logspace(np.log10(min_T), np.log10(max_T), 100)
    dJdE = 0. * E
    for i in range(len(E)):
        E_i = E[i]
        dJdE[i] += np.power(10., log_H(np.log10(E_i)))
        dJdE[i] += np.power(10., log_He(np.log10(E_i)))
        dJdE[i] += np.power(10., log_C(np.log10(E_i)))
        dJdE[i] += np.power(10., log_O(np.log10(E_i)))

    ax.plot(E, np.power(E, slope) * 1.22 * dJdE, color=color)
    print ("... plotted AMS-02 all-particle data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_KASCADEGrande(ax, slope, color, label):
    """
    KASCADE-Grande H spectrum
    column 1: E in [GeV]
    column 2: dJdE in [m􏰁^-2 sr􏰁^-1 s􏰁^-1 GeV^􏰁-1]
    column 3: UncertLow
    column 4: UncertHigh
    reference: Arteaga-Velázquez et al., ICRC (2017) 316
    url: https://pos.sissa.it/301/316
    note: from https://kcdc.ikp.kit.edu - model KG_SIBYLL-23_p
    """
    filename = 'data/H_KASCADE-Grande2017.txt'
    E, dJdE, err_lo, err_up = np.loadtxt(filename, skiprows=2, usecols=(0,1,2,3), unpack=True)
    E /= 1e9 # GeV
    dJdE *= 1e9 # GeV^-1
    err_lo *= 1e9
    err_up *= 1e9
    errorbar_H(ax, E, dJdE, [err_lo, err_up], slope, color)
    print ("... plotted KASCADE-Grande H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_KASCADE(ax, slope, color, label):
    """
    KASCADE H spectrum
    column 1: E in [GeV]
    column 2: dJdE in [m􏰁^-2 sr􏰁^-1 s􏰁^-1 GeV^􏰁-1]
    column 3: UncertLow
    column 4: UncertHigh
    reference: Antoni et al., Astroparticle Physics (2005) 24
    url: https://www.sciencedirect.com/science/article/pii/S0927650505000691
    note: from https://kcdc.ikp.kit.edu - model KAS_QGSjet01_proton
    """
    filename = 'data/H_KASCADE2005_QGSJET.txt'
    E, dJdE, err_lo, err_up = np.loadtxt(filename, skiprows=2, usecols=(0,1,2,3), unpack=True)
    E /= 1e9 # GeV
    dJdE *= 1e9 # GeV^-1
    err_lo *= 1e9
    err_up *= 1e9
    errorbar_H(ax, E, dJdE, [err_lo, err_up], slope, color)
    print ("... plotted KASCADE H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_ICETOP(ax, slope, color, label):
    """
    ICETOP H spectrum
    column 1: log10(E/GeV)
    column 2: Flux in [GeV-1 m-2 s-1 sr-1]
    column 3: stat
    column 4: syst_down
    column 5: syst_up
    reference: Aartsen et al., Phys.Rev.D (2019) 100
    url: https://doi.org/10.1103/PhysRevD.100.082002
    note: Table IV
    """
    filename = 'data/H_IceTop2019.txt'
    log10E, dJdE, stat, syst_do, syst_up = np.loadtxt(filename, skiprows=1, usecols=(0,1,2,3,4), unpack=True)
    E = np.power(10., log10E)
    dJdE_err_lo = np.sqrt(stat * stat + syst_do * syst_do)
    dJdE_err_up = np.sqrt(stat * stat + syst_up * syst_up)
    dJdE_err = [dJdE_err_lo, dJdE_err_up]
    errorbar_H(ax, E, dJdE, dJdE_err, slope, color)
    print ("... plotted ICETOP H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_CALET(ax, slope, color, label):
    """
    CALET H spectrum
    reference: Adriani et al., Phys.Rev.Lett. (2019) 122
    url: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.181102
    note: dataset from SSDC database
    """
    filename = 'data/p_CALET_PRL2019_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted CALET H data between %6.2e and %6.2e GeV" % (min(E), max(E)))
    
def H_DAMPE(ax, slope, color, label):
    """
    DAMPE H spectrum
    reference: DAMPE Collaboration, Science Advances (2019) 5
    url: https://advances.sciencemag.org/content/5/9/eaax3793
    note: dataset from SSDC database
    """
    filename = 'data/p_DAMPE_SCIENCE2019_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted DAMPE H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_CREAM(ax, slope, color, label):
    """
    CREAM H spectrum
    reference: Yoon et al., ApJ (2017) 839
    url: https://iopscience.iop.org/article/10.3847/1538-4357/aa68e4/pdf
    note: dataset from SSDC database
    """
    filename = 'data/p_flux_CREAMIII_ApJ2017_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted CREAM H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_PAMELA(ax, slope, color, label):
    """
    PAMELA H spectrum
    reference: Adriani et al., Science (2011) 332
    url: https://science.sciencemag.org/content/332/6025/69.abstract
    note: dataset from SSDC database
    """
    filename = 'data/p_PAM_Sci2011_kin_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    dJdE *= (100. - 3.2) / 100.
    err_low *= (100. - 3.2) / 100.
    err_high *= (100. - 3.2) / 100.
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted PAMELA H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_AMS(ax, slope, color, label):
    """
    AMS-02 H spectrum
    reference: Aguilar et al., Phys.Rev.Lett. (2015) 114
    url: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.114.171103
    note: dataset from SSDC database
    """
    xml_filename = 'data/p_AMS_PRL2015_ekin_000.xml'
    E = get_column_from_xml('kinetic_energy', xml_filename)
    dJdE = get_column_from_xml('flux', xml_filename)
    err_low = get_column_from_xml('flux_total_error_low', xml_filename)
    err_high = get_column_from_xml('flux_total_error_high', xml_filename)
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted AMS-02 H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def H_BESS(ax, slope, color, label):
    """
    """
    filename = 'data/p_BESS-PolarI_ApJ2016_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar_H(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted BESS-PolarI H data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def leptons_AMS02(ax, slope, color, label):
    """
    AMS-02 electron+positron spectrum
    from SSDC database
    reference: AMS collaboration, Phys.Rev.Lett. (2019) 122
    """
    filename = 'data/e+e-_AMS_PRL2019_ekin_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted AMS-02 lepton data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def leptons_DAMPE(ax, slope, color, label):
    """
    DAMPE electron+positron spectrum
    from SSDC database
    reference: DAMPE Collaboration, Nature (2017) 552
    """
    filename = 'data/e+e-_DAMPE_NATURE2017_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted DAMPE lepton data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def leptons_CALET(ax, slope, color, label):
    """
    CALET electron+positron spectrum
    from SSDC database
    reference: Adriani et al., Phys.Rev.Lett. (2018) 120
    """
    filename = 'data/e+e-_CALET_PRL2018_binningDAMPE_ekin_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted CALET lepton data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def leptons_HESS(ax, slope, color, label):
    """
    HESS electron+positron spectrum
    from SSDC database
    reference: Aharonian et al., Phys.Rev.Lett. (2008) 101
    """
    xml_filename = 'data/e+e-_HESS_PRL2008_HE_000.xml'
    E = get_column_from_xml('kinetic_energy', xml_filename)
    dJdE = get_column_from_xml('flux', xml_filename)
    err_low = get_column_from_xml('flux_statistical_error_low', xml_filename)
    err_high = get_column_from_xml('flux_statistical_error_high', xml_filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted HESS lepton data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def positrons_AMS02(ax, slope, color, label):
    """
    AMS-02 positron spectrum
    from SSDC database
    reference: AMS collaboration, Phys.Rev.Lett. (2019) 122
    """
    filename = 'data/e+_AMS_PRL2019_ekin_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted AMS-02 positron data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def positrons_PAMELA(ax, slope, color, label):
    """
    PAMELA positron spectrum
    from SSDC database
    reference: Adriani et al., Phys.Rev.Lett. (2013) 111
    """
    filename = 'data/e+_PAMELA_PRL2013_ekin_000.xml'
    E, dJdE, err_low, err_high = read_ssdc(filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted PAMELA positron data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def antiprotons_PAMELA(ax, slope, color, label):
    """
    PAMELA antiproton spectrum
    from SSDC database
    reference: Adriani et al., JETP Letters, 2012, Vol. 96
    """
    xml_filename = 'data/pbar_PAM_JETPlett2013_000.xml'
    E = get_column_from_xml('kinetic_energy', xml_filename)
    dJdE = get_column_from_xml('flux', xml_filename)
    err_low = get_column_from_xml('flux_total_error_low', xml_filename)
    err_high = get_column_from_xml('flux_total_error_high', xml_filename)
    errorbar(ax, E, dJdE, [err_low, err_high], slope, color)
    print ("... plotted PAMELA antiproton data between %6.2e and %6.2e GeV" % (min(E), max(E)))

def antiprotons_AMS02(ax, slope, color, label):
    """
    """
    filename = 'data/pbar_AMS_PRL2016_000.xml'
    rigidity_min = get_column_from_xml('rigidity_min', filename)
    rigidity_max = get_column_from_xml('rigidity_max', filename)
    R = np.sqrt(rigidity_min * rigidity_max)
    dJdR = get_column_from_xml('flux', filename)
    stat_low = get_column_from_xml('flux_statistical_error_low', filename)
    stat_high = get_column_from_xml('flux_statistical_error_high', filename)
    sys_low = get_column_from_xml('flux_systematical_error_low', filename)
    sys_high = get_column_from_xml('flux_systematical_error_high', filename)
    err_low = np.sqrt(stat_low * stat_low + sys_low * sys_low)
    err_high = np.sqrt(stat_high * stat_high + sys_high * sys_high)
    errorbar(ax, R, dJdR, [err_low, err_high], slope, color)
    print ("... plotted AMS-02 antiproton data between %6.2e and %6.2e GeV" % (min(R), max(R)))

def gamma_FERMI_IGRB(ax, color, label):
    filename = 'data/EGB_Fermi.txt'
    E_min, E_max, f_igrb, errh_igrb, errl_igrb = np.loadtxt(filename, skiprows=24, usecols=(0,1,2,3,4), unpack=True)
    E = np.sqrt(E_min * E_max) / 1e3 # GeV
    x, y = E, E * f_igrb * 1e4
    y_err = E * errh_igrb * 1e4
    ax.errorbar(x, y, yerr=y_err, fmt='o', markeredgecolor=color, color=color,elinewidth=2, capthick=2, mfc='white')

def gamma_FERMI_diffuse(ax, color, label):
    E_1, f_1 = np.loadtxt('data/FERMI_DIFFUSE_1.txt', skiprows=0, usecols=(0,1), unpack=True)
    E_2, f_2 = np.loadtxt('data/FERMI_DIFFUSE_2.txt', skiprows=0, usecols=(0,1), unpack=True)
    E_3, f_3 = np.loadtxt('data/FERMI_DIFFUSE_3.txt', skiprows=0, usecols=(0,1), unpack=True)
    x = (np.array(E_1) + np.array(E_2) + np.array(E_3)) / 3.
    y = np.array(f_1) + np.array(f_2) + np.array(f_3)
    ax.plot(x / 1e3, y * 1e4 / 1e3, 'o', mfc='white', markersize=7, markeredgecolor=color, markeredgewidth=1.4, color=color)

def neutrinos_ICECUBE(ax, color, label):
    E = np.logspace(np.log10(2e4), np.log10(2e6), 100)
    flux = 1.57e-18 * pow(E / 1e5, -2.48) * 1e4 # m^-2 s^-1 sr^-1

    flux_min = (1.57e-18 - 0.22e-18) * pow(E / 1e5, -2.48 - 0.08) * 1e4 # m^-2 s^-1 sr^-1
    flux_max = (1.57e-18 + 0.23e-18) * pow(E / 1e5, -2.48 + 0.08) * 1e4 # m^-2 s^-1 sr^-1

    x = [6.1e4, 9.6e4, 3e6]
    y_min = [2.3e-4, 1.7e-4, 2.5e-6]
    y_max = [6e-4, 3.4e-4, 3.8e-5]
    ax.fill_between(np.array(x), 3. * np.array(y_min), 3. * np.array(y_max), facecolor=color, alpha=0.4, lw=2, edgecolor=color)

    x = [1.2e5, 4.65e6]
    y_min = [7.4e-5, 2.6e-5]
    y_max = [1.2e-4, 8.8e-5]
    ax.fill_between(np.array(x), 3. * np.array(y_min), 3. * np.array(y_max), facecolor=color, alpha=0.4, lw=2, edgecolor=color)
