This folder contains scripts for running the experiments described in they study. The types of results are

- Diversities
- Diversity rates-of-change

When getting a particular result, the service for the result type will try to find the result in persisted storage. If it fails, the result will be calculated and stored for future queries.

Each result is uniquely identified by all the parameters required to obtain it, as well as an "experiment number", allowing multiple results to be obtained and stored for each experiment configuration. The parameters associated with the types are described below.

## Diversities

A diversity measurement is unique with regards to

- An experiment number (typically, 30 results are taken per configuration)
- A configuration, consisting of
    - A PSO algorithm
    - The population size of the PSO algorithm
    - A benchmark function
    - The dimensionality of the benchmark function
    - The number of iterations (swarm-wide position updates) the PSO runs through before stopping

## Diversity Rates-of-Change

A DRoC measurement is unique with regards to

- An experiment number (typically, 30 results are taken per configuration)
- A configuration, consisting of
    - A PSO algorithm
    - The population size of the PSO algorithm
    - A benchmark function
    - The dimensionality of the benchmark function
    - The number of iterations (swarm-wide position updates) the PSO runs through before stopping

## TODO

- Add results type for comparing two algorithms' DRoCs for otherwise the same configuration
- Uniquely identify each diversity result by its iteration
- Do not uniquely identify each diversity result by the total number of iterations; instead, always calculate up to the max number of iterations (I think 20k is a safe bet, we'll probably only go up to 10k).