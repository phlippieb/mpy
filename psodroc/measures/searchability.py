import numpy as np


def FCIs(function, domain_min, domain_max, dimensions):
    # Performs the following sets of fitness cloud index measurements:
    # - 30 x FCI_soc measurements (with social-only PSO updates)
    # - 30 x FCI_cog measurements (with cognitive-only PSO updates)
    # Returns the following:
    # 1. The mean of the FCI_soc measurements
    # 2. The mean of the FCI_cog measurements
    # 3. The mean of the standard deviation of the FCI_soc and the FCI_cog measurements, respectively.

    num_samples = 30
    swarm_size = 16

    fci_socs = [FCI_soc(function, domain_min, domain_max, dimensions, swarm_size)
                for _ in range(num_samples)]

    fci_cogs = [FCI_cog(function, domain_min, domain_max, dimensions, swarm_size)
                for _ in range(num_samples)]

    fci_soc_mean = np.mean(fci_socs)
    fci_cog_mean = np.mean(fci_cogs)
    fci_sigma = FCI_sigma(fci_socs, fci_cogs)

    return fci_soc_mean, fci_cog_mean, fci_sigma


def FCI_sigma(FCI_socs, FCI_cogs):
    # Given a list each of FCI_soc and FCI_cog measurements,
    # this determines the standard deviation of each list of measurements
    # and returns the mean of those standard deviations.
    FCI_soc_dev = np.std(FCI_socs)
    FCI_cog_dev = np.std(FCI_cogs)
    return np.mean(FCI_soc_dev, FCI_cog_dev)


import pso.social_only_pso as spso


def FCI_soc(function, domain_min, domain_max, dimensions, swarm_size):
    spso.init_pso_defaults()
    spso.init_swarm(swarm_size)


def FCI_cog(function, domain_min, domain_max, dimensions, swarm_size):
    return 1.
