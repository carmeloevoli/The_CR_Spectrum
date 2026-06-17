import math
from pathlib import Path

import numpy as np
from utils import write_data_to_file

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / 'source'
OUTPUT_DIR = BASE_DIR / 'output'

MESE_DATAFILE = 'IceCube2026_mese.csv'
MESE_OUTPUT_DATAFILE = 'IceCube_nus_mese_energy.txt'

COMBINEDFIT_DATAFILE = 'IceCube2026_combinedfit.csv'
COMBINEDFIT_OUTPUT_DATAFILE = 'IceCube_nus_combinedfit_energy.txt'

GLASHOW_DATAFILE = 'IceCube2021_Glashow.csv'
GLASHOW_OUTPUT_DATAFILE = 'IceCube_nus_glashow_energy.txt'

GP_KRA5_DATAFILE = 'IceCube2023_nus_gp_kra5.txt'
GP_KRA5_OUTPUT_DATAFILE = 'IceCube_nus_gp_kra5_energy.txt'

GP_KRA50_DATAFILE = 'IceCube2023_nus_gp_kra50.txt'
GP_KRA50_OUTPUT_DATAFILE = 'IceCube_nus_gp_kra50_energy.txt'

KM3NET_DATAFILE = 'KM3NeT2025_km3_230213A.csv'
KM3NET_OUTPUT_DATAFILE = 'KM3NeT_nus_km3_230213A_energy.txt'

ALL_FLAVOUR_FACTOR = 3.0
GP_KRA5_UNCERTAINTY = (0.15 / 0.55, 0.18 / 0.55)
GP_KRA50_UNCERTAINTY = (0.11 / 0.37, 0.13 / 0.37)


def convert_icecube2026_csv(filename):
    x, xmin, xmax, y, y_lower, y_upper = np.loadtxt(
        filename, delimiter=',', comments='#', usecols=(0, 1, 2, 3, 4, 5), unpack=True
    )

    dxLo = np.abs(x - xmin)
    dxUp = np.abs(x - xmax)

    # CSV fluxes are in 1e-8 GeV cm^-2 s^-1 sr^-1 per flavour.
    # Convert to all-flavour GeV m^-2 s^-1 sr^-1.
    flux_scale = 1e-4 * ALL_FLAVOUR_FACTOR
    measured = y_lower > 0

    y_out = np.where(measured, y, y_upper) * flux_scale
    dyLo = np.where(measured, y - y_lower, 2.0 * y_upper) * flux_scale
    dyUp = np.where(measured, y_upper - y, 0.0) * flux_scale

    return x, dxLo, dxUp, y_out, dyLo, dyUp


def convert_km3net(filename):
    # Same CSV layout/units as the IceCube 2026 tables, but a single event row,
    # so force a 2-D load to keep the columns as arrays.
    x, xmin, xmax, y, y_lower, y_upper = np.loadtxt(
        filename, delimiter=',', comments='#', usecols=(0, 1, 2, 3, 4, 5),
        unpack=True, ndmin=2
    )

    dxLo = np.abs(x - xmin)
    dxUp = np.abs(x - xmax)

    flux_scale = 1e-4 * ALL_FLAVOUR_FACTOR
    measured = y_lower > 0

    y_out = np.where(measured, y, y_upper) * flux_scale
    dyLo = np.where(measured, y - y_lower, 2.0 * y_upper) * flux_scale
    dyUp = np.where(measured, y_upper - y, 0.0) * flux_scale

    return x, dxLo, dxUp, y_out, dyLo, dyUp


def convert_mese(filename):
    return convert_icecube2026_csv(filename)


def convert_combinedfit(filename):
    return convert_icecube2026_csv(filename)


def convert_glashow(filename):
    xmin, xmax, y, y_lower, y_upper = np.loadtxt(
        filename, delimiter=',', comments='#', usecols=(0, 1, 2, 3, 4), unpack=True
    )

    x = np.sqrt(xmin * xmax)
    dxLo = np.abs(x - xmin)
    dxUp = np.abs(x - xmax)

    # CSV fluxes are in 1e-8 GeV cm^-2 s^-1 sr^-1 per flavour.
    # Convert to all-flavour GeV m^-2 s^-1 sr^-1.
    flux_scale = 1e-4 * ALL_FLAVOUR_FACTOR
    measured = y_lower > 0

    y_out = np.where(measured, y, y_upper) * flux_scale
    dyLo = np.where(measured, y - y_lower, 2.0 * y_upper) * flux_scale
    dyUp = np.where(measured, y_upper - y, 0.0) * flux_scale

    return x, dxLo, dxUp, y_out, dyLo, dyUp


def convert_gp(filename, uncertainty_low, uncertainty_up):
    x, y = np.loadtxt(
        filename, comments='#', usecols=(0, 1), unpack=True
    )
    
    # Source values are E^2 F in GeV cm^-2 s^-1. Convert to
    # all-flavour GeV m^-2 s^-1 sr^-1 assuming the flux is all-sky.
    y_out = y * 1e4 / (4.0 * math.pi) * ALL_FLAVOUR_FACTOR
    dyLo = y_out * uncertainty_low
    dyUp = y_out * uncertainty_up
    return x, np.zeros_like(x), np.zeros_like(x), y_out, dyLo, dyUp


def write_converted_table(outputfile, x, dxLo, dxUp, y, dyLo, dyUp):
    header = (f'#E - dE_lo - dE_up - y - dy_lo - dy_up\n')

    data_lines = [f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n' 
                for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(x, dxLo, dxUp, y, dyLo, dyUp)]

    write_data_to_file(outputfile, header, data_lines)


def convert_all():
    write_converted_table(
        OUTPUT_DIR / MESE_OUTPUT_DATAFILE,
        *convert_mese(SOURCE_DIR / MESE_DATAFILE),
    )
    write_converted_table(
        OUTPUT_DIR / COMBINEDFIT_OUTPUT_DATAFILE,
        *convert_combinedfit(SOURCE_DIR / COMBINEDFIT_DATAFILE),
    )
    write_converted_table(
        OUTPUT_DIR / GLASHOW_OUTPUT_DATAFILE,
        *convert_glashow(SOURCE_DIR / GLASHOW_DATAFILE),
    )
    write_converted_table(
        OUTPUT_DIR / GP_KRA5_OUTPUT_DATAFILE,
        *convert_gp(SOURCE_DIR / GP_KRA5_DATAFILE, *GP_KRA5_UNCERTAINTY),
    )
    write_converted_table(
        OUTPUT_DIR / GP_KRA50_OUTPUT_DATAFILE,
        *convert_gp(SOURCE_DIR / GP_KRA50_DATAFILE, *GP_KRA50_UNCERTAINTY),
    )
    write_converted_table(
        OUTPUT_DIR / KM3NET_OUTPUT_DATAFILE,
        *convert_km3net(SOURCE_DIR / KM3NET_DATAFILE),
    )


if __name__ == '__main__':
    convert_all()
