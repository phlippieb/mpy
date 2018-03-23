/*
    DIVERSITY
    ---------
    Data points are diversity measurements taken during a PSO's execution on a benchmark.
    Each measurement is taken for a particular configuration (consisting of a 
    specific PSO algorithm with a specific swarm size and a specific benchmark function 
    in a specific dimensionality), at a particular iteration or timestamp of the PSO's execution.
    Multiple (repeated) experiments can be run for a single configuration. Results from 
    different experiments are differentiated by the experiment column.
*/

CREATE TABLE diversity(
    pso_name VARCHAR(32) NOT NULL, -- Name of the PSO algorithm associated with this experiment
    swarm_size INTEGER NOT NULL, -- Number of particles in the PSO associated with this experiment
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function associated with this experiment
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function associated with this experiment
    iteration INTEGER NOT NULL, -- The iteration or timestamp of the experiment that this diversity measurement was taken at
    experiment INTEGER NOT NULL, -- The numbered experiment (so we can take multiple samples, eg. 30)
    diversity DOUBLE PRECISION NOT NULL, -- The diversity result
    
    PRIMARY KEY(pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment)
);

/*
    DIVERSITY RATES OF CHANGE
    -------------------------
    Data points are computed rates-of-change of all diversity measurements taken during a
    single experiment (with a particular configuration). Each experiment yields one DRoC.
    DRoC measurements may be dependent on the number of iterations that the PSO was executed for
    (or equivalently, the number of iterations included in the DRoC calculation), so the number 
    of iterations forms part of the configuration.
*/
CREATE TABLE droc(
    pso_name VARCHAR(32) NOT NULL, -- Name of the PSO algorithm associated with this experiment
    swarm_size INTEGER NOT NULL, -- Number of particles in the PSO associated with this experiment
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function associated with this experiment
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function associated with this experiment
    iterations INTEGER NOT NULL, -- Number of iterations included in the DRoC calculation
    experiment INTEGER NOT NULL, -- The numbered experiment (so we can take multiple samples, eg. 30)
    droc DOUBLE PRECISION NOT NULL, -- The DRoC result
    
    PRIMARY KEY(pso_name, swarm_size, benchmark_name, dimensionality, iterations, experiment)
);
