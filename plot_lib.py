import matplotlib
import matplotlib.pyplot as plt
import numpy as np
    
eV2Joule = 1.60218e-19

matplotlib.rc("savefig", dpi=200)

def ax_settings(ax):
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.7)
    ax.minorticks_on()
    ax.tick_params('both', length=15, width=1.7, which='major', pad=10)
    ax.tick_params('both', length=0,  width=1.7, which='minor', pad=10)

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

def set_plot_style():
    #plt.style.use('bmh')
    matplotlib.rcParams.update({
        #'axes.grid': True,
        #'axes.titlesize': 'medium',
        'errorbar.capsize': 3,
        'font.family': 'serif',
        'font.serif': 'Palatino',
        'font.size': 28,
        #'grid.color': 'w',
        #'grid.linestyle': '-',
        #'grid.alpha': 0.5,
 	    #'grid.linewidth': 1,
 	    'legend.frameon': False,
 	    'legend.fancybox': False,
 	    'legend.fontsize': 20,
 	    #'legend.framealpha': 0.7,
 	    #'legend.handletextpad': 0.1,
 	    #'legend.labelspacing': 0.2,
 	    'legend.loc': 'best',
        'legend.numpoints': 1,
        'lines.linewidth': 3,
        'lines.markersize' : 6,
        'savefig.bbox': 'tight',
 	    #'savefig.pad_inches': 0.02,
        'figure.autolayout': True,
 	    'text.usetex': True,
 	    #'text.latex.preamble': r'\usepackage{txfonts}',
        'xtick.labelsize': 26,
        'ytick.labelsize': 26,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'axes.labelpad': 12,
 	})
    fig = plt.figure(figsize=(10.0, 10.5))
    ax = fig.add_subplot(1, 1, 1)
    ax_settings(ax)
    return fig, ax

