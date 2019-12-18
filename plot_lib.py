import matplotlib
import matplotlib.pyplot as plt
import numpy as np
    
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
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.7)
    ax.minorticks_on()
    ax.tick_params('both', length=15, width=1.7, which='major', pad=10)
    ax.tick_params('both', length=0,  width=1.7, which='minor', pad=10)
    return fig, ax

matplotlib.rc("savefig", dpi=200)
