import numpy as np
from extract_crdb import write_data_to_file

def convert_table(filename, outputfile):
    x, f_lo, f, f_up = np.loadtxt('tables/' + filename, usecols=(0,1,2,3), unpack=True)
    x /= 1e3 # MeV -> GeV
    dxLo = .0 * x
    dxUp = .0 * x
    y = f * 1e1 # GeV/m2/s/sr
    dyLo = np.abs(f - f_lo) * 1e1 # GeV/m2/s/sr
    dyUp = np.abs(f - f_up) * 1e1 # GeV/m2/s/sr
    
    # Prepare data for file writing
    header = (f'#E - dE_lo - dE_up - y - dy_lo - dy_up\n')

    data_lines = [f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n' 
                for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(x, dxLo, dxUp, y, dyLo, dyUp)]

    write_data_to_file('tables/' + outputfile, header, data_lines)

if __name__ == '__main__':
    convert_table('FERMI_gammas_inner.txt', 'FERMI_inner_energy.txt')
