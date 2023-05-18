from PlotFuncs import TheCrSpectrum, MySaveFig

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

MySaveFig(fig, 'The_CR_Spectrum_2023', True)
