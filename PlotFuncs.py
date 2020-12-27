import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('./allcrs.mplstyle')
import numpy as np
import math

def MySaveFig(fig, pltname, pngsave=False):
    if pngsave:
        filename = pltname + '.png'
    else:
        filename = pltname + '.pdf'
    print ("Saving plot as " + filename)
    fig.savefig(filename, bbox_inches='tight', dpi=300)
    
class TheCrSpectrum():
    cAMS02 = 'forestgreen'
    cAUGER = 'steelblue'
    cBESS = 'yellowgreen'
    cCALET = 'darkcyan'
    cCREAM = 'r'
    cDAMPE = 'm'
    cFERMI = 'b'
    cHAWC = 'slategray'
    cHESS = 'darkorchid'
    cICECUBE = 'salmon'
    cICETOP_ICECUBE = 'c'
    cKASCADEGrande = 'goldenrod'
    cKASCADE = 'darkgoldenrod'
    cNUCLEON = 'sienna'
    cPAMELA = 'darkorange'
    cTA = 'crimson'
    cTIBET = 'indianred'
    cTUNKA = 'hotpink'
    cVERITAS = 'seagreen'
    
    def __init__(self):
         print ("Calling TheCrSpectrum constructor")
    
    def FigSetup(self, Shape='Rectangular'):
        if Shape=='Wide':
            fig = plt.figure(figsize=(16.5,5))
        elif Shape=='Rectangular':
            fig = plt.figure(figsize=(10.0,10.5))
        ax = fig.add_subplot(111)
        self.SetAxes(ax)
        return fig,ax

    def SetAxes(self, ax):
        #Set x-axis
        ax.minorticks_off()
        ax.set_xscale('log')
        ax.set_xlim([1, 1e12])
        ax.set_xticks(np.logspace(0, 12, 13))
        labels = ['GeV', '', '', 'TeV', '', '', 'PeV', '', '', 'EeV', '', '']
        ax.set_xticklabels(labels)
        ax.set_xlabel('Energy')
        #Set y-axis
        ax.set_yscale('log')
        ax.set_ylim([1e-7, 1e4])
        ax.set_ylabel(r'Energy flux [GeV/m$^2$ s sr]')
        #Set twin y-axis
        ax2 = ax.twiny()
        ax2.minorticks_off()
        ax2.set_xscale('log')
        ax2.set_xlabel('Energy [J]', color='tab:blue', labelpad=20)
        eV2Joule = 1.60218e-19
        ax2.set_xlim([1e9 * eV2Joule, 1e21 * eV2Joule])
        ax2.set_xticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0, 1e2])
        ax2.tick_params(axis='x', colors='tab:blue')
    
    def plot_line(self, ax, filename, color):
        E, dJdE = np.loadtxt(filename,skiprows=7,usecols=(0,1),unpack=True)
        ax.plot(E, np.power(E, 2.0) * dJdE, color=color)
        
    def plot_data(self, ax, filename, fmt, color, zorder=1):
        E, dJdE, err_low, err_high = np.loadtxt(filename,skiprows=3,usecols=(0,1,2,3),unpack=True)
        size = len(E)
        for i in range(size):
            y = np.power(E[i], 2.0) * dJdE[i]
            dJdE_err = .5 * (err_low[i] + err_high[i])
            yerr = np.power(E[i], 2.0) * dJdE_err
            if (yerr < y):
                ax.errorbar(E[i], y, yerr=yerr, fmt=fmt, markeredgecolor=color, color=color, elinewidth=2, capthick=2, zorder=zorder)
            #else:
            #    ax.errorbar(E[i], y, yerr=0.4*y, uplims=True, fmt=fmt, markeredgecolor=color, color=color, elinewidth=2, capsize=0)

    def annotate(self, ax):
        E_LHC = 2. * np.power(13e3, 2) / 0.938
        ax.annotate('LHC', xy=(E_LHC, 1e-7), xytext=(E_LHC, 1e-6), horizontalalignment="center",
        arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
        )
        ax.annotate('Knee', xy=(2.8e6, 1.), xytext=(1e5, 9e-2),
        arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
        )
        ax.annotate('Ankle', xy=(0.7e10, 4e-4), xytext=(1.25e10, 3e-3),
        arrowprops=dict(facecolor='slategrey', edgecolor='slategrey', shrink=0.05), fontsize=19
        )
        
        E = np.logspace(0, 15)
        EdNdE = 1. # 1 m2/s
        E2dNdEdOmega = E * EdNdE / 4. / math.pi
        ax.text(0.4e4, 0.8e3, r'1/m$^2$/s', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0,
                        facecolor='tab:gray', edgecolor='tab:gray')

        EdNdE = 1. / 3.14e7 # 1 m2/yr
        E2dNdEdOmega = E * EdNdE / 4. / math.pi
        ax.text(4e10, 0.3e3, r'1/m$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0,
                        facecolor='tab:gray', edgecolor='tab:gray')

        EdNdE = 1. / 3.14e7 / 1e6 # 1 km2/yr
        E2dNdEdOmega = E * EdNdE / 4. / math.pi
        ax.text(2.25e10, 1.6e-4, r'1/km$^2$/yr', fontsize=16, color='tab:gray', rotation=50)
        ax.fill_between(E, E2dNdEdOmega, 1e4, alpha=0.12, lw=0,
                        facecolor='tab:gray', edgecolor='tab:gray')

        ax.fill_between(E, E2dNdEdOmega, 1e-10, alpha=0.06, lw=0,
                        facecolor='tab:gray', edgecolor='tab:gray')

        ax.text(0.5e2, 6e0, r'$e^-$+$e^+$', fontsize=22)
        ax.text(0.85e1, 2e0, r'$e^+$', fontsize=22)
        ax.text(2.2, 1.4e-2, r'$\bar{p}$', fontsize=22)
        ax.text(7, 0.7e3, r'$p$', fontsize=22)
        ax.text(0.5e7, 3e-5, r'$\nu + \bar{\nu}$', fontsize=21)
        ax.text(0.5e2, 2e-2, r'$\gamma$', fontsize=21)
        ax.text(0.9e3, 3e-5, r'$\gamma$ IRGB', fontsize=20)
        #ax.text(0.6e3, 4e2, r'$\sim E^{-2.7}$')
        #ax.text(5.5e8, 1e-2, r'$\sim E^{-3.1}$')
    
    def ypos(self, i):
        f_text = 1.90
        return 0.020 * pow(f_text, i)
        
    def experiment_legend(self, ax):
        font_size = 13
        ax.text(1.1e9, self.ypos(18), 'AMS-02', color=self.cAMS02, fontsize=font_size)
        ax.text(1.1e9, self.ypos(17), 'AUGER', color=self.cAUGER, fontsize=font_size)
        ax.text(1.1e9, self.ypos(16), 'BESS', color=self.cBESS, fontsize=font_size)
        ax.text(1.1e9, self.ypos(15), 'CALET', color=self.cCALET, fontsize=font_size)
        ax.text(1.1e9, self.ypos(14), 'CREAM', color=self.cCREAM, fontsize=font_size)
        ax.text(1.1e9, self.ypos(13), 'DAMPE', color=self.cDAMPE, fontsize=font_size)
        ax.text(1.1e9, self.ypos(12), 'FERMI', color=self.cFERMI, fontsize=font_size)
        ax.text(1.1e9, self.ypos(11), 'HAWC', color=self.cHAWC, fontsize=font_size)
        ax.text(1.1e9, self.ypos(10), 'HESS', color=self.cHESS, fontsize=font_size)
        ax.text(1.1e9, self.ypos(9), 'ICECUBE', color=self.cICECUBE, fontsize=font_size)
        ax.text(1.1e9, self.ypos(8), 'ICETOP+ICECUBE', color=self.cICETOP_ICECUBE, fontsize=font_size)
        ax.text(1.1e9, self.ypos(7), 'KASCADE', color=self.cKASCADE, fontsize=font_size)
        ax.text(1.1e9, self.ypos(6), 'KASCADE-Grande', color=self.cKASCADEGrande, fontsize=font_size)
        ax.text(1.1e9, self.ypos(5), 'NUCLEON', color=self.cNUCLEON, fontsize=font_size)
        ax.text(1.1e9, self.ypos(4), 'PAMELA', color=self.cPAMELA, fontsize=font_size)
        ax.text(1.1e9, self.ypos(3), 'Telescope Array', color=self.cTA, fontsize=font_size)
        ax.text(1.1e9, self.ypos(2), 'Tibet-III', color=self.cTIBET, fontsize=font_size)
        ax.text(1.1e9, self.ypos(1), 'TUNKA', color=self.cTUNKA, fontsize=font_size)
        ax.text(1.1e9, self.ypos(0), 'VERITAS', color=self.cVERITAS, fontsize=font_size)
    
    def positrons(self, ax):
        pdir = 'data/positrons/'
        self.plot_data(ax, pdir+'e+_FERMI_Ek.txt', 'o', self.cFERMI, 1)
        self.plot_data(ax, pdir+'e+_AMS-02_Ek.txt', 'o', self.cAMS02, 2)
        self.plot_data(ax, pdir+'e+_PAMELA_Ek.txt', 'o', self.cPAMELA, 3)

    def antiprotons(self, ax):
        pdir = 'data/antiprotons/'
        self.plot_data(ax, pdir+'H-bar_BESS_Ek.txt', 'o', self.cBESS, 3)
        self.plot_data(ax, pdir+'H-bar_AMS-02_Ek.txt', 'o', self.cAMS02, 1)
        self.plot_data(ax, pdir+'H-bar_PAMELA_Ek.txt', 'o', self.cPAMELA, 2)

    def leptons(self, ax):
        pdir = 'data/leptons/'
        self.plot_data(ax, pdir+'leptons_AMS-02_Ek.txt', 'o', self.cAMS02, 1)
        self.plot_data(ax, pdir+'leptons_FERMI_Etot.txt', 'o', self.cFERMI, 4)
        self.plot_data(ax, pdir+'leptons_CALET_Etot.txt', 'o', self.cCALET, 3)
        self.plot_data(ax, pdir+'leptons_DAMPE_Etot.txt', 'o', self.cDAMPE, 5)
        self.plot_data(ax, pdir+'leptons_VERITAS_Etot.txt', 'o', self.cVERITAS, 2)
        #ADD HESS DATA?

    def protons(self, ax):
        pdir = 'data/protons/'
        self.plot_data(ax, pdir+'H_KASCADE_2005_SIBYLL-2.1_Etot.txt', 'P', self.cKASCADE)
        self.plot_data(ax, pdir+'H_BESS-TeV_Ek.txt', 'P', self.cBESS)
        self.plot_data(ax, pdir+'H_PAMELA_Ek.txt', 'P', self.cPAMELA)
        self.plot_data(ax, pdir+'H_AMS-02_Ek.txt', 'P', self.cAMS02)
        self.plot_data(ax, pdir+'H_CREAM-III_Ek.txt', 'P', self.cCREAM)
        self.plot_data(ax, pdir+'H_KASCADEGrande_SIBYLL-2.3_Etot.txt', 'P', self.cKASCADEGrande)
        self.plot_data(ax, pdir+'H_ICECUBE-ICETOP_Etot.txt', 'P', self.cICETOP_ICECUBE)
        self.plot_data(ax, pdir+'H_NUCLEON_Etot.txt', 'P', self.cNUCLEON)
        self.plot_data(ax, pdir+'H_CALET_Ek.txt', 'P', self.cCALET)
        self.plot_data(ax, pdir+'H_DAMPE_Ek.txt', 'P', self.cDAMPE)

    def allparticle(self, ax):
        pdir = 'data/allparticle/'
        self.plot_data(ax, pdir+'allparticle_AUGER_Etot.txt', 'o', self.cAUGER)
        self.plot_data(ax, pdir+'allparticle_TA_Etot.txt', 'o', self.cTA)
        self.plot_data(ax, pdir+'allparticle_TIBET_QGSJET+HD_Etot.txt', 'o', self.cTIBET)
        self.plot_data(ax, pdir+'allparticle_HAWC_Etot.txt', 'o', self.cHAWC)
        self.plot_data(ax, pdir+'allparticle_ICECUBE-ICETOP_SIBYLL-2.1_Etot.txt', 'o', self.cICETOP_ICECUBE)
        self.plot_data(ax, pdir+'allparticle_KASCADEGrande_SIBYLL-2.3_Etot.txt', 'o', self.cKASCADEGrande)
        self.plot_data(ax, pdir+'allparticle_KASCADE_SIBYLL-2.1_Etot.txt', 'o', self.cKASCADE)
        self.plot_data(ax, pdir+'allparticle_NUCLEON_Etot.txt', 'o', self.cNUCLEON)
        self.plot_data(ax, pdir+'allparticle_TUNKA-133_Etot.txt', 'o', self.cTUNKA)
#        self.plot_data(ax, pdir+'allparticle_ICETOP_E_2019.txt', 'o', self.cICETOP)
#        self.plot_line(ax, pdir+'allparticle_AMS02.txt', self.cAMS02)
#        self.plot_line(ax, pdir+'allparticle_CREAM.txt', self.cCREAM)

    def gammas(self, ax):
        pdir = 'data/gammas/'
        E, y, y_err = np.loadtxt(pdir+'gamma_igrb_FERMI.txt',skiprows=3,usecols=(0,1,2),unpack=True)
        ax.errorbar(E, y, yerr=y_err, fmt='o',
                    markeredgecolor=self.cFERMI, color=self.cFERMI, elinewidth=2, capthick=2, mfc='white')
        E, y = np.loadtxt(pdir+'gamma_diffuse_FERMI.txt',skiprows=3,usecols=(0,1),unpack=True)
        ax.plot(E, y, 'o', markeredgecolor=self.cFERMI, markeredgewidth=1.4, color=self.cFERMI, mfc='white')

    def neutrinos(self, ax):
        color = self.cICECUBE
        
        E = np.logspace(np.log10(2e4), np.log10(2e6), 100)
        flux = 1.57e-18 * pow(E / 1e5, -2.48) * 1e4 # m^-2 s^-1 sr^-1

        flux_min = (1.57e-18 - 0.22e-18) * pow(E / 1e5, -2.48 - 0.08) * 1e4 # m^-2 s^-1 sr^-1
        flux_max = (1.57e-18 + 0.23e-18) * pow(E / 1e5, -2.48 + 0.08) * 1e4 # m^-2 s^-1 sr^-1

        x = [6.1e4, 9.6e4, 3e6]
        y_min = [2.3e-4, 1.7e-4, 2.5e-6]
        y_max = [6e-4, 3.4e-4, 3.8e-5]
        ax.fill_between(np.array(x), 3. * np.array(y_min), 3. * np.array(y_max), alpha=0.4, lw=2,
                        facecolor=color, edgecolor=color)

        x = [1.2e5, 4.65e6]
        y_min = [7.4e-5, 2.6e-5]
        y_max = [1.2e-4, 8.8e-5]
        ax.fill_between(np.array(x), 3. * np.array(y_min), 3. * np.array(y_max), alpha=0.4, lw=2,
                        facecolor=color, edgecolor=color)


