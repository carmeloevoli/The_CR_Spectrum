from pathlib import Path

import numpy as np
from utils import write_data_to_file

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / 'source'
OUTPUT_DIR = BASE_DIR / 'output'

FRACTION_DATAFILE = 'fractions_Sibyll2.3e_fit_stats_data_2025.txt'
OUTPUT_DATAFILE = 'AUGER_H_Sibyll2.3e_energy.txt'

# All-particle fit from Phys. Rev. Lett. 125, 121106 (2020),
# Eq. on page 5 of the APS PDF / arXiv:2008.06488.
J0 = 1.315e-18  # km^-2 sr^-1 yr^-1 eV^-1
E0 = 10**18.5  # eV
GAMMAS = (3.29, 2.51, 3.05, 5.10)
BREAKS = (5.0e18, 13.0e18, 46.0e18)  # eV
OMEGA = 0.05

SECONDS_PER_YEAR = 365.25 * 24.0 * 3600.0
EV_PER_GEV = 1e9
M2_PER_KM2 = 1e6


def auger_all_particle_flux_ev(energy_ev):
    """Return Auger's all-particle J(E) in km^-2 sr^-1 yr^-1 eV^-1."""
    flux = J0 * (energy_ev / E0) ** (-GAMMAS[0])

    for break_energy, gamma_before, gamma_after in zip(BREAKS, GAMMAS[:-1], GAMMAS[1:]):
        transition = 1.0 + (energy_ev / break_energy) ** (1.0 / OMEGA)
        flux *= transition ** ((gamma_before - gamma_after) * OMEGA)

    return flux


def convert_all_particle_flux_to_gev(flux_ev):
    """Convert dN/dE from eV^-1 km^-2 yr^-1 to GeV^-1 m^-2 s^-1."""
    return flux_ev * EV_PER_GEV / M2_PER_KM2 / SECONDS_PER_YEAR


def load_proton_fractions(filename):
    rows = []
    with Path(filename).open() as f:
        next(f)
        for line in f:
            if not line.strip() or line.startswith('*'):
                continue

            columns = line.split()
            if len(columns) < 11:
                continue

            element = int(columns[4])
            if element != 100:
                continue

            energy_min, energy_max, energy_avg = [float(value) for value in columns[:3]]
            fraction = float(columns[5])
            fraction_err_lo = float(columns[6])
            fraction_err_up = float(columns[7])
            rows.append((energy_min, energy_max, energy_avg, fraction, fraction_err_lo, fraction_err_up))

    return np.array(rows, dtype=float)


def convert_table(filename, outputfile):
    fractions = load_proton_fractions(filename)
    log_emin, log_emax, log_eavg, fraction, fraction_err_lo, fraction_err_up = fractions.T

    energy_ev = 10**log_eavg
    energy_gev = energy_ev / EV_PER_GEV
    emin_gev = 10**log_emin / EV_PER_GEV
    emax_gev = 10**log_emax / EV_PER_GEV
    dxLo = np.abs(energy_gev - emin_gev)
    dxUp = np.abs(energy_gev - emax_gev)

    all_particle_flux = convert_all_particle_flux_to_gev(auger_all_particle_flux_ev(energy_ev))
    energy2 = energy_gev**2

    measured = fraction_err_lo < fraction
    proton_flux = fraction * all_particle_flux
    proton_flux_lo = fraction_err_lo * all_particle_flux
    proton_flux_up = fraction_err_up * all_particle_flux

    upper_limit_flux = (fraction + fraction_err_up) * all_particle_flux
    y = np.where(measured, proton_flux, upper_limit_flux) * energy2
    dyLo = np.where(measured, proton_flux_lo, 2.0 * upper_limit_flux) * energy2
    dyUp = np.where(measured, proton_flux_up, 0.0) * energy2

    header = (
        '#E - dE_lo - dE_up - y - dy_lo - dy_up\n'
        '#E in GeV; y = E^2 J_p in GeV m^-2 s^-1 sr^-1\n'
        '#Proton fraction model: Sibyll2.3e, Element 100\n'
    )
    data_lines = [
        f'{x_:10.5e} {dxLo_:10.5e} {dxUp_:10.5e} {y_:10.5e} {dyLo_:10.5e} {dyUp_:10.5e}\n'
        for x_, dxLo_, dxUp_, y_, dyLo_, dyUp_ in zip(energy_gev, dxLo, dxUp, y, dyLo, dyUp)
    ]

    write_data_to_file(outputfile, header, data_lines)


if __name__ == '__main__':
    convert_table(SOURCE_DIR / FRACTION_DATAFILE, OUTPUT_DIR / OUTPUT_DATAFILE)
