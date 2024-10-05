import matplotlib
import platform
import matplotlib.pyplot as plt
import numpy as np
import math

# Use appropriate backend if on MacOS
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

# Set matplotlib style
plt.style.use('./allcrs.mplstyle')

# Utility function to save figure
def MySaveFig(fig, pltname, pngsave=False):
    print(f"Saving plot as {pltname}.pdf")
    if pngsave:
        fig.savefig(f"{pltname}.png", bbox_inches='tight', dpi=300)
    fig.savefig(f"{pltname}.pdf", bbox_inches='tight', dpi=300)

class TheCrSpectrum:
    """Class for plotting cosmic ray spectrum data."""
    
    # Experiment colors as a dictionary to avoid multiple attributes
    colors = {
        'AMS-02': 'forestgreen', 
        'AUGER': 'steelblue', 
        'BESS': 'yellowgreen',
        'CALET': 'darkcyan', 
        'CREAM': 'r', 
        'DAMPE': 'm', 
        'FERMI': 'b',
        'HAWC': 'slategray', 
        'HESS': 'darkorchid', 
        'IceCube': 'salmon',
        'ICETOP_ICECUBE': 'c', 
        'KASCADE': 'darkgoldenrod', 
        'KASCADE-Grande': 'goldenrod',
        'NUCLEON': 'sienna', 
        'PAMELA': 'darkorange', 
        'TA': 'crimson',
        'TIBET': 'indianred', 
        'TUNKA-133': 'hotpink', 
        'VERITAS': 'seagreen'
    }
    colors = dict(reversed(list(colors.items())))

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
        ax.set_xlim([1, 1e12])
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
        ax2.set_xlim([1e9 * eV2Joule, 1e21 * eV2Joule])
        ax2.set_xticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0, 1e2])
        ax2.tick_params(axis='x', colors='tab:blue')
    
    def annotate(self, ax):
        """Annotates specific points on the plot."""
        s_LHC = 14e3 # GeV
        proton_mass = 0.938 # GeV
        E_LHC = 2. * np.power(s_LHC, 2) / proton_mass
        annotations = [
            ('LHC', E_LHC, 1e-7, E_LHC, 1e-6),
            ('Knee', 2.8e6, 1., 2.5e5, 1.3e-1),
            ('Ankle', 0.7e10, 4e-4, 1.25e10, 3e-3),
        ]
        for text, x, y, xtext, ytext in annotations:
            ax.annotate(text, xy=(x, y), xytext=(xtext, ytext), horizontalalignment="center",
                        arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19)
        
        texts = [(r'$e^-$+$e^+$', 0.5e2, 6e0),
                 (r'$e^+$', 0.85e1, 2e0),
                 (r'$\bar{p}$', 2.2, 1.4e-2),
                 (r'$p$', 7, 0.7e3),
                 (r'$\nu + \bar{\nu}$', 0.5e6, 2.5e-4),
                 (r'$\gamma$', 0.5e2, 1.8e-2),
                 (r'$\gamma$ IGRB', 0.9e3, 3e-5),
        ]
        for text, x, y in texts:
            ax.text(x, y, text, fontsize=20)

        # Add fill between for the E2dNdEdOmega data
        E = np.logspace(0, 15)
        E2dNdEdOmega = E * 1. / 4. / math.pi # m2/s
        ax.text(0.4e4, 0.8e3, r'1/m$^2$/s', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        E2dNdEdOmega = E * 1. / 3.14e7 / 4. / math.pi # m2/yr
        ax.text(4e10, 0.3e3, r'1/m$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        E2dNdEdOmega = E * 1. / 3.14e7 / 1e6 / 4. / math.pi # km2/yr
        ax.text(2.25e10, 1.6e-4, r'1/km$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        ax.fill_between(E, E2dNdEdOmega, 1e-10, alpha=0.06, lw=0, facecolor='tab:gray', edgecolor='tab:gray')

        ax.text(1.1e12, 2e-1, r'github.com/carmeloevoli/The_CR_Spectrum', rotation=-90, fontsize=11, color='tab:gray')

    def experiment_legend(self, ax):
        """Adds legend for experiments."""
        for i, (exp, color) in enumerate(self.colors.items()):
            ax.text(1.1e9, self.ypos(i), exp, color=color, fontsize=13)

    def ypos(self, i):
        """Returns vertical position for experiment labels."""
        return 0.015 * pow(1.95, i)

    def plot_experiment_data(self, ax, experiment_type):
        """Plot function to handle different types of particles (positrons, antiprotons, etc.)"""
        data_files = {
            'positrons': ['AMS-02_e+_energy.txt', 
                          'FERMI_e+_energy.txt', 
                          'PAMELA_e+_energy.txt'],
            'antiprotons': ['AMS-02_pbar_energy.txt', 
                            'BESS_pbar_energy.txt', 
                            'PAMELA_pbar_energy.txt'],
            'leptons': ['AMS-02_e-e+_energy.txt', 
                        'CALET_e-e+_energy.txt', 
                        'DAMPE_e-e+_energy.txt',
                        'FERMI_e-e+_energy.txt', 
                        'HESS_e-e+_energy.txt'],
            'protons': ['AMS-02_H_energy.txt', 
                        'BESS_H_energy.txt', 
                        'CREAM_H_energy.txt',
                        'CALET_H_energy.txt', 
                        'DAMPE_H_energy.txt', 
                        'KASCADE_H_energy.txt',
                        'KASCADE-Grande_H_energy.txt', 
                        'PAMELA_H_energy.txt'],
            'allParticles' : ['AUGER_allParticles_energy.txt',
                              'HAWC_allParticles_energy.txt',
                              'KASCADE_allParticles_energy.txt',
                              'KASCADE-Grande_allParticles_energy.txt',
                              'NUCLEON_allParticles_energy.txt',
                              'IceCube_allParticles_energy.txt',
                              'TA_allParticles_energy.txt',
                              'TUNKA-133_allParticles_energy.txt'],
        }
        pdir = 'data/crdb/'
        if experiment_type in data_files:
            for filename in data_files[experiment_type]:
                self.plot_data(ax, f'{pdir}{filename}', 'o', self.colors[filename.split('_')[0]], 1)
        if experiment_type == 'allParticles':
            self.plot_line(ax, f'{pdir}AMS-02_allParticles_energy.txt', self.colors['AMS-02'])
            self.plot_line(ax, f'{pdir}CREAM_allParticles_energy.txt', self.colors['CREAM'])

    def neutrinos(self, ax):
        """Plot neutrino measurements with error bars."""
        filename = 'data/tables/IceCube_nus_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['IceCube'])

    def gammas(self, ax):
        """Plot ... with error bars."""
        filename = 'data/tables/FERMI_igrb_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['FERMI'])
        filename = 'data/tables/FERMI_inner_energy.txt'
        self.plot_data_diffuse(ax, filename, self.colors['FERMI'])

    def plot_data(self, ax, filename, fmt, color, zorder=1):
        """Plot data with error bars."""
        E, dJdE, errStatLo, errStatUp, errSysLo, errSysUp = np.loadtxt(
            filename, skiprows=8, usecols=(0, 1, 2, 3, 4, 5), unpack=True
        )
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

    def plot_line(self, ax, filename, color):
        """Plot a line for the all-particle spectrum."""
        E, dJdE = np.loadtxt(filename, usecols=(0, 1), unpack=True)
        ax.plot(E, E**2 * dJdE, color=color)

    def plot_data_diffuse(self, ax, filename, color):
        """Plot diffuse data."""
        x, dxLo, dxUp, y, dyLo, dyUp = np.loadtxt(filename, skiprows=1, usecols=(0, 1, 2, 3, 4, 5), unpack=True)
        ind = dyLo < y
        ax.errorbar(x[ind], y[ind], yerr=[dyLo[ind], dyUp[ind]], xerr=[dxLo[ind], dxUp[ind]],
                    fmt='o', markeredgecolor=color, color=color, elinewidth=1.5, capthick=1.5, mfc='white')
        ind_upper = dyLo > y
        ax.errorbar(x[ind_upper], y[ind_upper], xerr=[dxLo[ind_upper], dxUp[ind_upper]], yerr=0.25 * y[ind_upper], uplims=True,
                    fmt='o', markeredgecolor=color, color=color, elinewidth=1.5, capthick=1.5, mfc='white')
