import numpy as np

def make_data_nus(filename):
    E_min, E_max, dJdE, err_lo, err_up = np.loadtxt(filename,skiprows=2,usecols=(1,2,3,4,5),unpack=True)
    x = np.sqrt(E_min * E_max)
    size = len(x)
    xErrLo = (x - E_min)
    xErrUp = (E_max - x)
    y = 3. * dJdE * 1e4 # cm-2 -> m-2
    yErrLo = 3. * (dJdE - err_lo) * 1e4 # cm-2 -> m-2
    yErrUp = 3. * (err_up - dJdE) * 1e4 # cm-2 -> m-2
    f = open('IceCube_neutrinos.txt', 'w')
    f.write("#E - errLo - errUp [GeV] - E2I - errLo - errUp [GeV m-2 s-1 sr-1]\n")
    for i in range(size):
        if err_lo[i] > 1e-40:
            f.write(f'{x[i]:9.3e} {xErrLo[i]:9.3e} {xErrUp[i]:9.3e} {y[i]:9.3e} {yErrLo[i]:9.3e} {yErrUp[i]:9.3e}\n')
        else:
            f.write(f'{x[i]:9.3e} {xErrLo[i]:9.3e} {xErrUp[i]:9.3e} {y[i]:9.3e} {1} {1}\n')
    f.close()
    
def make_data_igrb(filename):
    Elo, Eup, fIGRB, dfUp, dfLo, dfDgUp, dfDgLo = np.loadtxt(filename,skiprows=61,max_rows=26, usecols=(1,2,3,4,5,6,7), unpack=True)
    Elo /= 1e3 # MeV -> GeV
    Eup /= 1e3 # MeV -> GeV
    x = np.sqrt(Elo * Eup)
    size = len(x)
    xErrLo = x - Elo
    xErrUp = Eup - x
    y = x * fIGRB * 1e4 # cm2 -> GeV m2
    yErrLo = x * (dfLo + dfDgLo) * 1e4 # cm2 -> GeV m2
    yErrUp = x * (dfUp + dfDgUp) * 1e4 # cm2 -> GeV m2
    f = open('FERMI_gammas_igrb.txt', 'w')
    f.write("#E - errLo - errUp [GeV] - E2I - errLo - errUp [GeV m-2 s-1 sr-1]\n")
    for i in range(size):
        f.write(f'{x[i]:9.3e} {xErrLo[i]:9.3e} {xErrUp[i]:9.3e} {y[i]:9.3e} {yErrLo[i]:9.3e} {yErrUp[i]:9.3e}\n')
    f.close()

def make_data_inner(filename):
    E, E2I = np.loadtxt(filename,usecols=(0,1),unpack=True)
    size = len(E)
    E /= 1e3 # MeV -> GeV
    E2I *= 1e1 # MeV cm-2 -> GeV m-2
    f = open('FERMI_gammas_inner.txt', 'w')
    f.write("#E [GeV] - E2I [GeV m-2 s-1 sr-1]\n")
    for i in range(size):
        f.write(f'{E[i]:9.3e} {E2I[i]:9.3e}\n')
    f.close()

if __name__== "__main__":
    make_data_nus('source/IceCube_neutrino_HESE_6yrs.txt')
    make_data_igrb('source/FERMI_gammas_igrb.txt')
    make_data_inner('source/FERMI_gammas_inner.txt')
    
