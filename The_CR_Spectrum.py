from PlotFuncs import TheCrSpectrum, MySaveFig

# Initialize the plot class
plot = TheCrSpectrum()

# Set up the figure and axes
fig, ax = plot.FigSetup()

# Plot different particle types using the new `plot_experiment_data` method
plot.plot_experiment_data(ax, 'positrons')
plot.plot_experiment_data(ax, 'antiprotons')
plot.plot_experiment_data(ax, 'leptons')
plot.plot_experiment_data(ax, 'protons')
plot.plot_experiment_data(ax, 'allParticles')

# Optionally plot gammas and neutrinos if needed by uncommenting the following lines:
# plot.gammas(ax)
# plot.neutrinos(ax)

# Add experiment legends and annotations
plot.experiment_legend(ax)
plot.annotate(ax)

# Save the figure
MySaveFig(fig, 'figures/The_CR_Spectrum_2024', pngsave=True)
