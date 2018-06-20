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

/* 
    DROC RANKS BETWEEN PSOs
    -----------------------
    Sets of DRoC measurements are compared between different PSOs (with all else being the same --
    same swarm size, benchmark function, dimensionality, and number of iterations). Comparisons are
    made between 30 DRoC measurements for each PSO, so the 30 configurations differentiated only by
    their experiment number are all taken into account in a single rank.
    A rank of -1 indicates that the first PSO's droc is significantly less than the second's; a rank of 1
    indicates that the first PSO's droc is significantly greater than the second's; and a 0 indicates no
    significant difference.
*/
CREATE TABLE droc_rank_between_psos(
    pso_1_name VARCHAR(32) NOT NULL, -- Name of the first PSO algorithm in the rank
    pso_2_name VARCHAR(32) NOT NULL, -- Name of the second PSO algorithm in the rank
    swarm_size INTEGER NOT NULL, -- Number of particles in the PSOs (same for both)
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function optimised by both PSOs
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function
    iterations INTEGER NOT NULL, -- Number of iterations included in the DRoC calculations
    rank_value INTEGER NOT NULL, -- The rank of PSO1 vs PSO2 (-1 indicating PSO1's DRoC is smaller)
    
    PRIMARY KEY(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, iterations)
);

/*
    FLC's
*/

/*
    RUGGEDNESS -- FEM 0.1
    ----------
*/
CREATE TABLE FEM_0_1(
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function being characterised
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function
    experiment INTEGER NOT NULL, -- The numbered experiment (so we can take multiple samples, eg. 30)
    measurement DOUBLE PRECISION NOT NULL, -- The ruggedness measurement

    PRIMARY KEY(benchmark_name, dimensionality, experiment)
);

/*
    RUGGEDNESS -- FEM 0.01
    ----------
*/
CREATE TABLE FEM_0_01(
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function being characterised
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function
    experiment INTEGER NOT NULL, -- The numbered experiment (so we can take multiple samples, eg. 30)
    measurement DOUBLE PRECISION NOT NULL, -- The ruggedness measurement

    PRIMARY KEY(benchmark_name, dimensionality, experiment)
);

/*
    NEUTRALITY -- PN
    ----------
*/

CREATE TABLE PN(
    benchmark_name VARCHAR(32) NOT NULL, -- Name of the benchmark function being characterised
    dimensionality INTEGER NOT NULL, -- Dimensionality of the benchmark function
    epsilon DOUBLE PRECISION NOT NULL, -- The neutrality error margin
    step_size_fraction DOUBLE PRECISION NOT NULL, -- The fraction of the search space domain used as a step size
    experiment INTEGER NOT NULL, -- The numbered experiment (so we can take multiple samples, eg. 30)
    measurement DOUBLE PRECISION NOT NULL, -- The ruggedness measurement

    PRIMARY KEY(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment)
)