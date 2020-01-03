#!/usr/bin/env python3
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import numpy as np

import plot_lib as plib
import plot_data as pdata

fig, ax = plib.set_plot_style()

color_AMS = 'forestgreen'
color_AUGER = 'steelblue'
color_BESS = 'y'
color_CALET = 'darkcyan'
color_CREAM = 'r'
color_DAMPE = 'm'
color_FERMI = 'b'
color_HAWC = 'slategray'
color_HESS = 'darkorchid'
color_ICECUBE = 'salmon'
color_ICETOP = 'seagreen'
color_ICETOP_ICECUBE = 'c'
color_KASCADEGrande = 'goldenrod'
color_PAMELA = 'darkorange'
color_TA = 'crimson'
color_TIBET = 'indianred'

# all particles
pdata.all_TA(ax, 2, color_TA, 'TA')
pdata.all_AUGER(ax, 2, color_AUGER, 'AUGER')
pdata.all_Tibet(ax, 2, color_TIBET, 'Tibet-III')
pdata.all_ICETOP(ax, 2, color_ICETOP, 'ICETOP')
pdata.all_ICETOP_ICECUBE(ax, 2, color_ICETOP_ICECUBE, 'ICETOP-ICECUBE')
pdata.all_KASCADEGrande(ax, 2, color_KASCADEGrande, 'KASCADE-Grande')
pdata.all_HAWC(ax, 2, color_HAWC, 'HAWC')
pdata.all_AMS(ax, 2, color_AMS, 'AMS')
pdata.all_CREAM(ax, 2, color_CREAM, 'CREAM')
print(' ')

# protons
pdata.H_ICETOP(ax, 2, color_ICETOP, 'ICETOP')
pdata.H_KASCADEGrande(ax, 2, color_KASCADEGrande, 'KG')
#pdata.H_KASCADE(ax, 2, color_KASCADE, 'KG')
pdata.H_CREAM(ax, 2, color_CREAM, 'CREAM')
pdata.H_CALET(ax, 2, color_CALET, 'DAMPE')
pdata.H_PAMELA(ax, 2, color_PAMELA, 'PAMELA')
pdata.H_AMS(ax, 2, color_AMS, 'AMS02')
pdata.H_BESS(ax, 2, color_BESS, 'BESS')
pdata.H_DAMPE(ax, 2, color_DAMPE, 'DAMPE')

print(' ')

# leptons
pdata.leptons_HESS(ax, 2, color_HESS, 'HESS')
pdata.leptons_DAMPE(ax, 2, color_DAMPE, 'DAMPE')
pdata.leptons_CALET(ax, 2, color_CALET, 'CALET')
pdata.leptons_AMS02(ax, 2, color_AMS, 'AMS02')
pdata.positrons_AMS02(ax, 2, color_AMS, 'AMS02')
pdata.positrons_PAMELA(ax, 2, color_PAMELA, 'PAMELA')
print(' ')

# antiprotons
pdata.antiprotons_AMS02(ax, 2, color_AMS, 'AMS02')
pdata.antiprotons_PAMELA(ax, 2, color_PAMELA, 'PAMELA')

# gamma
pdata.gamma_FERMI_diffuse(ax, color_FERMI, 'FERMI diffuse')
pdata.gamma_FERMI_IGRB(ax, color_FERMI, 'FERMI IGRB')
pdata.neutrinos_ICECUBE(ax, color_ICECUBE, 'FERMI IGRB')

ax.text(0.5e2, 6e0, r'$e^-$+$e^+$', fontsize=22)
ax.text(0.85e1, 2e0, r'$e^+$', fontsize=22)
ax.text(2.7, 1.1e-2, r'$\bar{p}$', fontsize=22)
ax.text(7, 0.7e3, r'$p$', fontsize=22)
ax.text(0.5e7, 3e-5, r'$\nu + \bar{\nu}$', fontsize=21)
ax.text(0.5e2, 2e-2, r'$\gamma$', fontsize=21)
ax.text(0.9e3, 3e-5, r'$\gamma$ IRGB', fontsize=20)
#ax.text(0.6e3, 4e2, r'$\sim E^{-2.7}$')
#ax.text(5.5e8, 1e-2, r'$\sim E^{-3.1}$')

E_LHC = 13e3**2 / 0.938
ax.annotate('LHC', xy=(E_LHC, 1e-7), xytext=(3.e6, 1e-6),
arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
)

ax.annotate('Knee', xy=(2.8e6, 1.), xytext=(1e5, 9e-2),
arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
)

ax.annotate('Ankle', xy=(0.7e10, 4e-4), xytext=(1.25e10, 3e-3),
arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
)

ax.text(1.4e2, 1.4e3, r'1/cm$^2$/s', fontsize=16, color='gray')

ax.text(6e6, 1.2, r'1/m$^2$/yr', fontsize=16, color='gray')

ax.text(1.9e10, 1.35 * 2.5e-4, r'1/km$^2$/yr', fontsize=16, color='gray')

f_text = 2.02

ax.text(1.1e9, 0.08 * pow(f_text, 15), 'AMS-02', color=color_AMS, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 14), 'AUGER', color=color_AUGER, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 13), 'BESS', color=color_BESS, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 12), 'CALET', color=color_CALET, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 11), 'CREAM', color=color_CREAM, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 10), 'DAMPE', color=color_DAMPE, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 9), 'FERMI', color=color_FERMI, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 8), 'HAWC', color=color_HAWC, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 7), 'HESS', color=color_HESS, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 6), 'ICECUBE', color=color_ICECUBE, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 5), 'ICETOP', color=color_ICETOP, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 4), 'ICETOP+ICECUBE', color=color_ICETOP_ICECUBE, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 3), 'KASCADE-Grande', color=color_KASCADEGrande, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 2), 'PAMELA', color=color_PAMELA, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 1), 'Telescope Array', color=color_TA, fontsize=14)
ax.text(1.1e9, 0.08 * pow(f_text, 0), 'Tibet-III', color=color_TIBET, fontsize=14)

plt.savefig('The_CR_spectrum.png',format='png',dpi=300)
