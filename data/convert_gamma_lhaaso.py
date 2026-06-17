from pathlib import Path

import numpy as np
from utils import write_data_to_file

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / 'source'
OUTPUT_DIR = BASE_DIR / 'output'

ORIGINAL_DATAFILE = 'LHAASO_KM2A_2023_TableS2_inner.txt'
OUTPUT_DATAFILE = 'LHAASO_gamma_inner_energy.txt'


def convert_table(filename, outputfile):
    log_emin, log_emax, energy_tev, phi, stat_lo, stat_up, sys = np.loadtxt(
        filename, usecols=(0, 1, 2, 3, 4, 5, 6), unpack=True
    )

    energy_gev = energy_tev * 1e3
    emin_gev = 10**log_emin * 1e3
    emax_gev = 10**log_emax * 1e3
    dxLo = np.abs(energy_gev - emin_gev)
    dxUp = np.abs(energy_gev - emax_gev)

    # TeV^-1 cm^-2 -> GeV^-1 m^-2.
    flux_gev = phi * 1e1
    stat_lo_gev = stat_lo * 1e1
    stat_up_gev = stat_up * 1e1
    sys_gev = sys * 1e1

    energy2 = energy_gev**2
    y = energy2 * flux_gev
    dyLo = energy2 * np.sqrt(stat_lo_gev**2 + sys_gev**2)
    dyUp = energy2 * np.sqrt(stat_up_gev**2 + sys_gev**2)

    header = '#E - dE_lo - dE_up - y - dy_lo - dy_up\n'
    data_lines = [
        f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n'
        for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(energy_gev, dxLo, dxUp, y, dyLo, dyUp)
    ]

    write_data_to_file(outputfile, header, data_lines)


if __name__ == '__main__':
    convert_table(SOURCE_DIR / ORIGINAL_DATAFILE, OUTPUT_DIR / OUTPUT_DATAFILE)
