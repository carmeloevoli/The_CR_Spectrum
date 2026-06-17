import matplotlib
import platform
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path

# Use appropriate backend if on MacOS
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

# Set matplotlib style
BASE_DIR = Path(__file__).resolve().parent
KISS_TABLES_DIR = BASE_DIR / 'kiss_tables'
DATA_OUTPUT_DIR = BASE_DIR / 'data' / 'output'

plt.style.use(BASE_DIR / 'allcrs.mplstyle')

# Utility function to save figure
def MySaveFig(fig, pltname, pngsave=False):
    if pngsave:
        fig.savefig(f"{pltname}.png", bbox_inches='tight', dpi=300)
        print(f"Saving plot as {pltname}.png")
    fig.savefig(f"{pltname}.pdf", bbox_inches='tight', dpi=300)
    print(f"Saving plot as {pltname}.pdf")

class TheCrSpectrum:
    """Class for plotting cosmic ray spectrum data."""
    proton_mass = 0.9382720813
    electron_mass = 0.00051099895

    species = {
        'H': {'A': 1, 'Z': 1, 'mass': proton_mass},
        'pbar': {'A': 1, 'Z': 1, 'mass': proton_mass},
        'e+': {'A': 1, 'Z': 1, 'mass': electron_mass},
        'e+e-': {'A': 1, 'Z': 1, 'mass': electron_mass},
        'He': {'A': 4, 'Z': 2, 'mass': 4 * proton_mass},
        'Li': {'A': 7, 'Z': 3, 'mass': 7 * proton_mass},
        'Be': {'A': 9, 'Z': 4, 'mass': 9 * proton_mass},
        'B': {'A': 11, 'Z': 5, 'mass': 11 * proton_mass},
        'C': {'A': 12, 'Z': 6, 'mass': 12 * proton_mass},
        'N': {'A': 14, 'Z': 7, 'mass': 14 * proton_mass},
        'O': {'A': 16, 'Z': 8, 'mass': 16 * proton_mass},
        'F': {'A': 19, 'Z': 9, 'mass': 19 * proton_mass},
        'Ne': {'A': 20, 'Z': 10, 'mass': 20 * proton_mass},
        'Na': {'A': 23, 'Z': 11, 'mass': 23 * proton_mass},
        'Mg': {'A': 24, 'Z': 12, 'mass': 24 * proton_mass},
        'Si': {'A': 28, 'Z': 14, 'mass': 28 * proton_mass},
        'S': {'A': 32, 'Z': 16, 'mass': 32 * proton_mass},
        'Fe': {'A': 56, 'Z': 26, 'mass': 56 * proton_mass},
        'allParticle': {'A': 1, 'Z': 1, 'mass': proton_mass},
    }
    
    # Experiment colors as a dictionary to avoid multiple attributes
    colors = {
        'AMS-02': '#00A651',
        'AUGER': '#0066FF',
        'BESS': '#F5A400',
        'CALET': '#00AEEF',
        'CREAM': '#FF2D20',
        'DAMPE': '#FF3DBE',
        'FERMI': '#0047FF',
        'HAWC': '#7A7A7A',
        'HESS': '#00B7EB',
        'IceCube': '#8A2BE2',
        'Icetop+Icecube': '#00C8B8',
        'KM3NeT': '#141E3C',
        'KASCADE': '#D49400',
        'KASCADE-Grande': '#C7A000',
        'LHAASO': '#FF1493',
        'NUCLEON': '#B35C00',
        'PAMELA': '#FF7A00',
        'TA': '#E60026',
        'TIBET': '#2ECC40',
        'TUNKA-133': '#A020F0',
        'VERITAS': '#76B900',
    }
    colors = dict(reversed(list(colors.items())))

    # Higher zorder values are drawn on top of lower values.
    zorders = {
        'AMS-02': 20,
        'AUGER': 19,
        'DAMPE': 18,
        'CALET': 17,
        'LHAASO': 16,
        'IceCube': 21,
        'KM3NeT': 22,
        'Icetop+Icecube': 14,
        'HAWC': 13,
        'FERMI': 12,
        'HESS': 11,
        'TA': 10,
        'CREAM': 9,
        'KASCADE': 8,
        'KASCADE-Grande': 7,
        'PAMELA': 6,
        'TIBET': 5,
        'TUNKA-133': 4,
        'NUCLEON': 3,
        'BESS': 2,
        'VERITAS': 1,
    }

    data_files = {
        'positrons': [
            ('AMS-02_e+_rigidity.txt', 'AMS-02', 'e+', 'rigidity'),
            #('FERMI_e+_kineticEnergy.txt', 'FERMI', 'e+', 'energy'),
            ('PAMELA_e+_kineticEnergy.txt', 'PAMELA', 'e+', 'energy'),
        ],
        'antiprotons': [
            ('AMS-02_pbar_rigidity.txt', 'AMS-02', 'pbar', 'rigidity'),
            ('PAMELA_pbar_kineticEnergy.txt', 'PAMELA', 'pbar', 'energy'),
        ],
        'leptons': [
            ('AMS-02_e+e-_rigidity.txt', 'AMS-02', 'e+e-', 'rigidity'),
            ('CALET_e+e-_totalEnergy.txt', 'CALET', 'e+e-', 'energy'),
            ('DAMPE_e+e-_totalEnergy.txt', 'DAMPE', 'e+e-', 'energy'),
            ('FERMI_e+e-_totalEnergy.txt', 'FERMI', 'e+e-', 'energy'),
            ('VERITAS_e+e-_totalEnergy.txt', 'VERITAS', 'e+e-', 'energy'),
        ],
        'protons': [
            ('AMS-02_H_rigidity.txt', 'AMS-02', 'H', 'rigidity'),
            ('BESS-TeV_H_kineticEnergy.txt', 'BESS', 'H', 'energy'),
            ('CREAM_H_kineticEnergy.txt', 'CREAM', 'H', 'energy'),
            ('CALET_H_kineticEnergy.txt', 'CALET', 'H', 'energy'),
            ('DAMPE_H_kineticEnergy.txt', 'DAMPE', 'H', 'energy'),
            ('LHAASO_SIBYLL-2.3d_H_totalEnergy.txt', 'LHAASO', 'H', 'energy'),
            ('IceTop_IceCube_SIBYLL-2.1_H_totalEnergy.txt', 'Icetop+Icecube', 'H', 'energy'),
            #('KASCADE_QGSJET-01_H_totalEnergy.txt', 'KASCADE', 'H', 'energy'),
            ('PAMELA_H_rigidity.txt', 'PAMELA', 'H', 'rigidity'),
        ],
        'allParticles': [
            ('HAWC_allParticle_totalEnergy.txt', 'HAWC', 'allParticle', 'energy'),
            ('NUCLEON_allParticle_totalEnergy.txt', 'NUCLEON', 'allParticle', 'energy'),
            ('KASCADE_2005_SIBYLL-2.1_allParticle_totalEnergy.txt', 'KASCADE', 'allParticle', 'energy'),
            ('KASCADE-Grande_QGSJet-II-04_allParticle_totalEnergy.txt', 'KASCADE-Grande', 'allParticle', 'energy'),
            ('IceTop_IceCube_SIBYLL-2.1_allParticle_totalEnergy.txt', 'Icetop+Icecube', 'allParticle', 'energy'),
            ('Auger_hybrid_allParticle_totalEnergy.txt', 'AUGER', 'allParticle', 'energy'),
            ('Tibet_SIBYLL+HD_allParticle_totalEnergy.txt', 'TIBET', 'allParticle', 'energy'),
            ('TUNKA-133_allParticle_totalEnergy.txt', 'TUNKA-133', 'allParticle', 'energy'),
            ('TALE_allParticle_totalEnergy.txt', 'TA', 'allParticle', 'energy'),
            ('TA_allParticle_totalEnergy.txt', 'TA', 'allParticle', 'energy'),
        ],
    }

    ams02_nuclei = [
        ('AMS-02_H_rigidity.txt', 'H', 'rigidity'),
        ('AMS-02_He_rigidity.txt', 'He', 'rigidity'),
        ('AMS-02_Li_rigidity.txt', 'Li', 'rigidity'),
        ('AMS-02_Be_rigidity.txt', 'Be', 'rigidity'),
        ('AMS-02_B_rigidity.txt', 'B', 'rigidity'),
        ('AMS-02_C_rigidity.txt', 'C', 'rigidity'),
        ('AMS-02_N_rigidity.txt', 'N', 'rigidity'),
        ('AMS-02_O_rigidity.txt', 'O', 'rigidity'),
        ('AMS-02_F_rigidity.txt', 'F', 'rigidity'),
        ('AMS-02_Ne_rigidity.txt', 'Ne', 'rigidity'),
        ('AMS-02_Na_rigidity.txt', 'Na', 'rigidity'),
        ('AMS-02_Mg_rigidity.txt', 'Mg', 'rigidity'),
        ('AMS-02_Si_rigidity.txt', 'Si', 'rigidity'),
        ('AMS-02_S_rigidity.txt', 'S', 'rigidity'),
        ('AMS-02_Fe_rigidity.txt', 'Fe', 'rigidity'),
    ]

    cream_nuclei = [
        ('CREAM_H_kineticEnergy.txt', 'H', 'energy'),
        ('CREAM_He_kineticEnergyPerNucleon.txt', 'He', 'energy_per_nucleon'),
        ('CREAM_C_kineticEnergyPerNucleon.txt', 'C', 'energy_per_nucleon'),
        ('CREAM_N_kineticEnergyPerNucleon.txt', 'N', 'energy_per_nucleon'),
        ('CREAM_O_kineticEnergyPerNucleon.txt', 'O', 'energy_per_nucleon'),
        ('CREAM_Ne_kineticEnergyPerNucleon.txt', 'Ne', 'energy_per_nucleon'),
        ('CREAM_Mg_kineticEnergyPerNucleon.txt', 'Mg', 'energy_per_nucleon'),
        ('CREAM_Si_kineticEnergyPerNucleon.txt', 'Si', 'energy_per_nucleon'),
        ('CREAM_Fe_kineticEnergyPerNucleon.txt', 'Fe', 'energy_per_nucleon'),
    ]

    def __init__(self):
        print("Initializing TheCrSpectrum")
    
    def FigSetup(self, shape='Rectangular'):
        """Sets up the figure based on the shape."""
        figsize = (16.5, 5) if shape == 'Wide' else (10.0, 10.5)
        fig, ax = plt.subplots(figsize=figsize)
        self.SetAxes(ax)
        return fig, ax

    def SetAxes(self, ax):
        """Configures the x and y axes for the plot."""
        ax.minorticks_off()
        ax.set_xscale('log')
        ax.set_xlim([.1, 1e12])
        ax.set_xticks([1e0, 1e3, 1e6, 1e9, 1e12])
        ax.set_xlabel('Energy [GeV]')
        ax.set_yscale('log')
        ax.set_ylim([1e-7, 1e4])
        ax.set_ylabel(r'E$^{2}$ Intensity [GeV m$^{-2}$ s$^{-1}$ sr$^{-1}$]')
        
        # Twin axis for Joules
        ax2 = ax.twiny()
        ax2.minorticks_off()
        ax2.set_xscale('log')
        ax2.set_xlabel('Energy [J]', color='tab:blue', labelpad=18)
        eV2Joule = 1.60218e-19
        ax2.set_xlim([.1 * 1e9 * eV2Joule, 1e21 * eV2Joule])
        ax2.set_xticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0, 1e2])
        ax2.tick_params(axis='x', colors='tab:blue')
    
    def annotate(self, ax):
        """Annotates specific points on the plot."""
        s_LHC = 14e3**2.0 # GeV2
        proton_mass = 0.938 # GeV
        E_LHC = 0.5 * s_LHC / proton_mass
        annotations = [
            ('LHC', E_LHC, 1e-7, E_LHC, 1e-6),
            ('Knee', 3.8e6, 1.5, 6.5e6, 1e1),
            ('Ankle', 0.7e10, 4e-4, 1.25e10, 3e-3),
        ]
        for text, x, y, xtext, ytext in annotations:
            ax.annotate(text, xy=(x, y), xytext=(xtext, ytext), horizontalalignment="center",
                        arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19, zorder=25)
        
        texts = [(r'$e^-$+$e^+$', 0.5e2, 6e0),
                 (r'$e^+$', 0.85e1, 2e0),
                 (r'$\bar{p}$', 0.25, 1.4e-2),
                 (r'$p$', 7, 0.7e3),
        ]
        for text, x, y in texts:
            ax.text(x, y, text, fontsize=20, zorder=25)

        # Diffuse datasets: label sits at (xtext, ytext) with a small arrow to (x, y) on the data
        diffuse_labels = [
            (r'$\nu + \bar{\nu}$', 0.5e6, 2.0e-3, 1.2e6, 2.4e-4),
            (r'$\gamma$ GP', 1.0e1, 1.2e-2, 1.0e1, 8.0e-2),
            (r'$\gamma$ GP', 9.8e5, 2.0e-6, 1.1e6, 2.05e-5),
            (r'$\nu + \bar{\nu}$ GP', 1.0e3, 5.0e-6, 1.1e4, 6.05e-5),
            (r'$\gamma$ IGRB', 4.0e0, 1.5e-5, 1.0e1, 2.1e-4),
        ]
        for text, xtext, ytext, x, y in diffuse_labels:
            ax.annotate(text, xy=(x, y), xytext=(xtext, ytext), fontsize=20, zorder=25,
                        arrowprops=dict(arrowstyle='->', color='black', lw=1.2,
                                        shrinkA=4, shrinkB=2))

        # Show N(>E) regions
        E = np.logspace(-1, 12) # GeV
        N = 1. # m-2 s-1
        E2I = 1.7 * N * E / 4. / math.pi # m-2 s-1 GeV sr-1
        ax.text(0.3e4, 0.8e3, r'1/m$^2$/s', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2I, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        N = 1. / 3.14e7 # m-2 yr-1
        E2I = 1.7 * N * E / 4. / math.pi # m-2 s-1 GeV sr-1
        ax.text(3.1e10, 0.3e3, r'1/m$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2I, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        N = 1. / 3.14e7 / 1e6 # km-2 yr-1
        E2I = 1.7 * N * E / 4. / math.pi # m-2 s-1 GeV sr-1
        ax.text(2.1e10, 1.95e-4, r'1/km$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2I, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        ax.fill_between(E, E2I, 1e-10, alpha=0.06, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        # Add credits
        ax.text(1.1e12, 2e-1, r'github.com/carmeloevoli/The_CR_Spectrum', rotation=-90, fontsize=11, color='tab:gray')

    def experiment_legend(self, ax):
        """Adds legend for experiments."""
        for i, (exp, color) in enumerate(self.colors.items()):
            ax.text(1.1e9, self.ypos(i), exp, color=color, fontsize=11)

    def ypos(self, i):
        """Returns vertical position for experiment labels."""
        return 0.010 * pow(1.92, i)

    def plot_experiment_data(self, ax, experiment_type):
        """Plot function to handle different types of particles (positrons, antiprotons, etc.)"""
        if experiment_type not in self.data_files:
            valid_types = ', '.join(sorted(self.data_files))
            raise ValueError(f"Unknown experiment type '{experiment_type}'. Expected one of: {valid_types}")

        for filename, color_key, species, x_kind in self.data_files[experiment_type]:
            self.plot_data(
                ax,
                KISS_TABLES_DIR / filename,
                'o',
                self.colors[color_key],
                self.zorders[color_key],
                species,
                x_kind,
            )

        if experiment_type == 'protons':
            self.auger_protons(ax)

        if experiment_type == 'allParticles':
            self.plot_summed_line(
                ax,
                self.ams02_nuclei,
                np.logspace(0.9, 3.1, 1000),
                self.colors['AMS-02'],
                self.zorders['AMS-02'],
            )
            self.plot_summed_line(
                ax,
                self.cream_nuclei,
                np.logspace(3.2, 4.8, 1000),
                self.colors['CREAM'],
                self.zorders['CREAM'],
            )

    def positrons(self, ax):
        self.plot_experiment_data(ax, 'positrons')

    def antiprotons(self, ax):
        self.plot_experiment_data(ax, 'antiprotons')

    def leptons(self, ax):
        self.plot_experiment_data(ax, 'leptons')

    def protons(self, ax):
        self.plot_experiment_data(ax, 'protons')

    def allparticle(self, ax):
        self.plot_experiment_data(ax, 'allParticles')

    def auger_protons(self, ax):
        """Plot the Auger proton spectrum inferred from mass-composition fractions."""
        filename = DATA_OUTPUT_DIR / 'AUGER_H_Sibyll2.3e_energy.txt'
        self.plot_data_diffuse(
            ax,
            filename,
            self.colors['AUGER'],
            self.zorders['AUGER'],
            markerfacecolor=self.colors['AUGER'],
        )

    def neutrinos(self, ax):
        """Plot neutrino measurements with error bars."""
        band_zorder = self.zorders['IceCube'] - 2
        self.plot_data_band(
            ax,
            DATA_OUTPUT_DIR / 'IceCube_nus_gp_kra5_energy.txt',
            color=self.colors['IceCube'],
            zorder=band_zorder,
            ls=':',
        )
        self.plot_data_band(
            ax,
            DATA_OUTPUT_DIR / 'IceCube_nus_gp_kra50_energy.txt',
            color=self.colors['IceCube'],
            zorder=band_zorder,
            ls='-',
        )

        filenames = [
            DATA_OUTPUT_DIR / 'IceCube_nus_mese_energy.txt',
            #DATA_OUTPUT_DIR / 'IceCube_nus_combinedfit_energy.txt',
            #DATA_OUTPUT_DIR / 'IceCube_nus_glashow_energy.txt',
        ]
        for filename in filenames:
            self.plot_data_diffuse(ax, filename, self.colors['IceCube'], self.zorders['IceCube'])

        self.km3net(ax)

    def km3net(self, ax):
        """Plot the single KM3-230213A ultra-high-energy neutrino event."""
        self.plot_data_diffuse(
            ax,
            DATA_OUTPUT_DIR / 'KM3NeT_nus_km3_230213A_energy.txt',
            self.colors['KM3NeT'],
            self.zorders['KM3NeT'],
        )

    def gammas(self, ax):
        """Plot gamma measurements with error bars."""
        filename = DATA_OUTPUT_DIR / 'FERMI_gamma_igrb_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['FERMI'], self.zorders['FERMI'])
        filename = DATA_OUTPUT_DIR / 'FERMI_gamma_inner_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['FERMI'], self.zorders['FERMI'])
        filename = DATA_OUTPUT_DIR / 'LHAASO_gamma_inner_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['LHAASO'], self.zorders['LHAASO'])

    def load_spectrum(self, filename, species, x_kind):
        """Load a KISS spectrum and convert x/y to differential flux vs GeV."""
        x, dJdx, errStatLo, errStatUp, errSysLo, errSysUp = np.loadtxt(
            filename, usecols=(0, 1, 2, 3, 4, 5), unpack=True
        )
        info = self.species[species]

        if x_kind == 'rigidity':
            mass = info['mass']
            charge = info['Z']
            energy = np.sqrt((charge * x)**2 + mass**2) - mass
            jacobian = (energy + mass) / (charge**2 * x)
        elif x_kind == 'energy_per_nucleon':
            energy = info['A'] * x
            jacobian = 1.0 / info['A']
        elif x_kind == 'energy':
            energy = x
            jacobian = 1.0
        else:
            raise ValueError(f"Unknown x_kind '{x_kind}' for {filename}")

        return (
            energy,
            dJdx * jacobian,
            errStatLo * jacobian,
            errStatUp * jacobian,
            errSysLo * jacobian,
            errSysUp * jacobian,
        )

    def plot_data(self, ax, filename, fmt, color, zorder=1, species='H', x_kind='energy'):
        """Plot data with error bars."""
        E, dJdE, errStatLo, errStatUp, errSysLo, errSysUp = self.load_spectrum(filename, species, x_kind)
        E2 = E * E
        y = E2 * dJdE
        dyLo = E2 * np.sqrt(errStatLo**2 + errSysLo**2)
        dyUp = E2 * np.sqrt(errStatUp**2 + errSysUp**2)

        ind = dyLo < y
        ax.errorbar(E[ind], y[ind], yerr=[dyLo[ind], dyUp[ind]], fmt=fmt, markeredgecolor=color,
                    color=color, elinewidth=1.5, capthick=1.5, zorder=zorder)

        ind_upper = dyLo > y
        ax.errorbar(E[ind_upper], y[ind_upper], yerr=0.25 * y[ind_upper], uplims=True,
                    fmt=fmt, markeredgecolor=color, color=color, elinewidth=1.5, capthick=1.5, zorder=zorder)

    def plot_line(self, ax, filename, color, zorder=1):
        """Plot a line for the all-particle spectrum."""
        E, dJdE = np.loadtxt(filename, usecols=(0, 1), unpack=True)
        ax.plot(E, E**2 * dJdE, color=color, zorder=zorder)

    def plot_summed_line(self, ax, datasets, E, color, zorder=1):
        """Plot an all-particle line by summing interpolated nuclei spectra."""
        total_flux = np.zeros_like(E)
        for filename, species, x_kind in datasets:
            energy, flux, *_ = self.load_spectrum(KISS_TABLES_DIR / filename, species, x_kind)
            log_flux = np.interp(np.log(E), np.log(energy), np.log(flux), left=-100, right=-100)
            total_flux += np.exp(log_flux)
        ax.plot(E, E**2 * total_flux, color=color, zorder=zorder)

    def plot_data_band(self, ax, filename, color, ls='-', zorder=1, alpha=0.18):
        """Plot a model curve as a solid line with a shaded uncertainty band."""
        x, _, _, y, dyLo, dyUp = np.loadtxt(filename, usecols=(0, 1, 2, 3, 4, 5), unpack=True)
        y_min = np.clip(y - dyLo, 1e-300, None)
        y_max = y + dyUp

        ax.fill_between(x, y_min, y_max, color=color, alpha=alpha, lw=0, zorder=zorder)
        ax.plot(x, y, color=color, lw=2.0, ls=ls, zorder=zorder + 0.1)

    def plot_data_diffuse(self, ax, filename, color, zorder=1, markerfacecolor='white'):
        """Plot diffuse data."""
        x, dxLo, dxUp, y, dyLo, dyUp = np.loadtxt(filename, usecols=(0, 1, 2, 3, 4, 5), unpack=True)
        ind = dyLo < y
        ax.errorbar(x[ind], y[ind], yerr=[dyLo[ind], dyUp[ind]], xerr=[dxLo[ind], dxUp[ind]],
                    fmt='o', markeredgecolor=color, color=color, elinewidth=1.5, capthick=1.5,
                    mfc=markerfacecolor, zorder=zorder)
        ind_upper = dyLo > y
        ax.errorbar(x[ind_upper], y[ind_upper], xerr=[dxLo[ind_upper], dxUp[ind_upper]], yerr=0.25 * y[ind_upper], uplims=True,
                    fmt='o', markeredgecolor=color, color=color, elinewidth=1.5, capthick=1.5,
                    mfc=markerfacecolor, zorder=zorder)
