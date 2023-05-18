import pytest
from PlotFuncs import TheCrSpectrum

@pytest.mark.mpl_image_compare(tolerance=0.5, savefig_kwargs={'dpi':300})
def test_allparticle_plot():
    
    plot = TheCrSpectrum()
    fig, ax = plot.FigSetup()
    plot.positrons(ax)
    plot.leptons(ax)
    plot.protons(ax)
    plot.antiprotons(ax)
    plot.allparticle(ax)
    plot.gammas(ax)
    plot.neutrinos(ax)
    plot.experiment_legend(ax)
    plot.annotate(ax)
    
    return fig