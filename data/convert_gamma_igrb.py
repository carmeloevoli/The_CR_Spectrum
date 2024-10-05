import numpy as np
from extract_crdb import write_data_to_file

# https://cdsarc.cds.unistra.fr/ftp/J/ApJ/799/86/ReadMe

def convert_table(filename, outputfile):
    x_min, x_max, f, f_up, f_lo, f_mod_up, f_mod_lo = np.loadtxt('tables/' + filename, usecols=(1,2,3,4,5,6,7), max_rows=26, unpack=True)
    x_min /= 1e3 # MeV -> GeV
    x_max /= 1e3 # MeV -> GeV
    x = np.sqrt(x_min * x_max)
    dxLo = np.abs(x - x_min)
    dxUp = np.abs(x - x_max)
    y = x * f * 1e4 # GeV/m2/s/sr
    dyLo = x * (f_up + f_mod_up) * 1e4
    dyUp = x * (f_lo + f_mod_lo) * 1e4
    # Prepare data for file writing
    header = (f'#E - dE_lo - dE_up - y - dy_lo - dy_up\n')

    data_lines = [f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n' 
                for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(x, dxLo, dxUp, y, dyLo, dyUp)]

    write_data_to_file('tables/' + outputfile, header, data_lines)

if __name__ == '__main__':
    convert_table('table3.dat', 'FERMI_igrb_energy.txt')
