#!/usr/bin/env python3
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import numpy as np

import plot_lib as plib
import plot_data as pdata

eV2Joule = 1.60218e-19

def ax_settings(ax):
    ax.set_xscale('log')
    ax.set_xlabel('Energy')
    ax.set_xlim([1, 1e12])
    ax.set_ylim([1e-7, 1e4])

    ax.set_xticks(np.logspace(0, 12, 13))
    labels = ['GeV', '', '', 'TeV', '', '', 'PeV', '', '', 'EeV', '', '']
    ax.set_xticklabels(labels)

    ax.set_yscale('log')
    ax.set_ylabel(r'Energy flux [GeV/m$^2$ s sr]')

    ax2 = ax.twiny()  # instantiate a second axes that shares the same x-axis
    ax2.set_xscale('log')
    ax2.set_xlabel('Energy [J]', color='steelblue', fontsize=26, labelpad=20)
    ax2.set_xlim([1e9 * eV2Joule, 1e21 * eV2Joule])
    ax2.tick_params('both', length=15, width=1.5, which='major', pad=5)
    ax2.tick_params('both', length=0,  width=1.3, which='minor', pad=5)
    ax2.set_xticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0, 1e2])
    ax2.tick_params(axis='x', colors='steelblue', labelsize=26)

fig, ax = plib.set_plot_style()

ax_settings(ax)

# all particles
pdata.TA_allparticle(ax, 'r', 'TA')
pdata.AUGER_allparticle(ax, 'steelblue', 'AUGER')
pdata.KASCADEGrande_allparticle(ax, 'm', 'KASCADE-Grande')
pdata.Tibet_allparticle(ax, 'y', 'Tibet-III')
pdata.ICETOP_allparticle(ax, 'b', 'ICETOP')
pdata.HAWC_allparticle(ax, 'g', 'HAWC')

# gamma
#pdata.FERMI_diffuse_gamma(ax, 'b', 'FERMI diffuse')
#pdata.FERMI_IGRB_gamma(ax, 'b', 'FERMI IGRB')

plt.savefig('The_CR_spectrum.png',format='png',dpi=300)
