from pathlib import Path

import numpy as np
from utils import write_data_to_file

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / 'source'
OUTPUT_DIR = BASE_DIR / 'output'

FERMI_IGRB_REPOSITORY_URL = 'https://cdsarc.cds.unistra.fr/ftp/J/ApJ/799/86/'
IGRB_ORIGINAL_DATAFILE = 'table3.dat'
IGRB_OUTPUT_DATAFILE = 'FERMI_gamma_igrb_energy.txt'

INNER_ORIGINAL_DATAFILE = 'Ackermann2012_diffuse_Fig17.txt'
INNER_OUTPUT_DATAFILE = 'FERMI_gamma_inner_energy.txt'

# IGRB_ORIGINAL_DATAFILE is the unmodified Table 3 data file from the Fermi
# repository above. INNER_ORIGINAL_DATAFILE is extracted from Fig. 17 of
# Ackermann et al. 2012. Both are converted to the common plotting table format.


def write_converted_table(outputfile, x, dxLo, dxUp, y, dyLo, dyUp):
    header = '#E - dE_lo - dE_up - y - dy_lo - dy_up\n'
    data_lines = [
        f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n'
        for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(x, dxLo, dxUp, y, dyLo, dyUp)
    ]
    write_data_to_file(outputfile, header, data_lines)


def convert_igrb(filename, outputfile):
    x_min, x_max, f, f_up, f_lo, f_mod_up, f_mod_lo = np.loadtxt(
        filename, usecols=(1, 2, 3, 4, 5, 6, 7), max_rows=26, unpack=True
    )
    x_min /= 1e3  # MeV -> GeV
    x_max /= 1e3  # MeV -> GeV
    x = np.sqrt(x_min * x_max)
    dxLo = np.abs(x - x_min)
    dxUp = np.abs(x - x_max)
    y = x * f * 1e4  # GeV m^-2 s^-1 sr^-1
    dyLo = x * (f_up + f_mod_up) * 1e4
    dyUp = x * (f_lo + f_mod_lo) * 1e4

    write_converted_table(outputfile, x, dxLo, dxUp, y, dyLo, dyUp)


def convert_inner(filename, outputfile):
    x, f_lo, f, f_up = np.loadtxt(filename, usecols=(0, 1, 2, 3), unpack=True)
    x /= 1e3  # MeV -> GeV
    dxLo = 0.0 * x
    dxUp = 0.0 * x
    y = f * 1e1  # GeV m^-2 s^-1 sr^-1
    dyLo = np.abs(f - f_lo) * 1e1
    dyUp = np.abs(f - f_up) * 1e1

    write_converted_table(outputfile, x, dxLo, dxUp, y, dyLo, dyUp)


def convert_all():
    convert_igrb(SOURCE_DIR / IGRB_ORIGINAL_DATAFILE, OUTPUT_DIR / IGRB_OUTPUT_DATAFILE)
    convert_inner(SOURCE_DIR / INNER_ORIGINAL_DATAFILE, OUTPUT_DIR / INNER_OUTPUT_DATAFILE)


if __name__ == '__main__':
    convert_all()
