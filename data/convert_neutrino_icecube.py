import numpy as np
from extract_crdb import write_data_to_file

def convert_table(filename, outputfile):
    xmin, x, xmax, ymin, y, ymax = np.loadtxt('tables/' + filename, usecols=(0,1,2,3,4,5), unpack=True)

    dxLo = np.abs(x - xmin)
    dxUp = np.abs(x - xmax)
    dyLo = np.abs(y - ymin)
    dyUp = np.abs(y - ymax)

    cms2ms = 1e4

    y *= cms2ms
    dyLo *= cms2ms
    dyUp *= cms2ms

    # Prepare data for file writing
    header = (f'#E - dE_lo - dE_up - y - dy_lo - dy_up\n')

    data_lines = [f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n' 
                for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(x, dxLo, dxUp, y, dyLo, dyUp)]

    write_data_to_file('tables/' + outputfile, header, data_lines)

if __name__ == '__main__':
    convert_table('IceCube_nus_showers.txt', 'IceCube_nus_energy.txt')
