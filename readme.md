# About
This is a library that provides PSO algorithms, optimisation benchmark functions, and stuff that measures several properties of both. I am writing this to perform experiments for my master's thesis on links between diversity rate-of-change of PSOs and the fitness landscape characteristics of the objective functions that they optimise.

## Structure
The `psodroc` package contains modules for PSO algorithms under `pso` and benchmark functions under `benchmark`. The project root contains an example script that runs the algorithms.

Each benchmark is in a file called `<benchmark name>.py`. In each benchmark file, the actual function implementation is in a function called `function(xs)`, which takes a candidate solution vector as a parameter. Each file also provides the benchmark's domain through functions called `min(d)` and `max(d)`, which respectively return the minimum and maximum allowed `x` value in dimension `d`.

# Install
This library uses python 2.7 with `numpy`, `scipy`, `numba`, and `matplotlib.pyplot`, as well as `pytest` for unit tests. Additionally, to explore and plot data, I recommend using `jupyter` notebooks. To get all of that, you can install [miniconda](http://conda.pydata.org/miniconda.html), and then use the conda package manager to install components.

Get a [download link](https://www.anaconda.com/download/#linux) for Anaconda (for Python 2.7!), or use one of these

Platform   | Download link
---        | ---
Ubuntu x64 | https://repo.continuum.io/archive/Anaconda2-5.1.0-Linux-x86_64.sh
Ubuntu x32 | https://repo.continuum.io/archive/Anaconda2-5.1.0-Linux-x86.sh
MacOS      | https://repo.continuum.io/archive/Anaconda2-5.1.0-MacOSX-x86_64.sh

Download and install it:
```
wget "<link>" -O install_anaconda.sh
bash install_anaconda.sh
source ~/.bashrc
```

Then install the required packages:
```
# Required:
conda install numba numpy psycopg2 pytest scipy

# If you're using pyplot:
conda install matplotlib

# If you're using Jupyter:
conda install jupyter
```

This library also uses a PostgreSQL database to manage results. For setup instructions, see the readme in the `db` directory.

# Run
The project contains a makefile, which can be used to run some basic commands:
- `make run` runs a file named `run.py`, which is used as the main entrypoint for the project.
- `make clean` removes temporary files.
- `make test` runs all unit tests using `pytest`.

The run script currently calculates all DRoC scripts. There are many of them, so it supports running batches. To run a batch, do e.g. 
```
python run.py --block 0 --of 5
```
This will run the first of 5 equally large batches.

To benchmark a sample of runs, do
```
python run.py --benchmark
```

# Coding style
Instead of aiming to create an elegant, generic, extensible library, I opted to make the code straight-forward and clear. My chosen approach can be summed up as "clarity over elegance". This especially caused me to reject DRY (don't repeat yourself) in favour of defining each algorithm, benchmark and measurement as an independent script. There will be lots of repeated code, but any part of the library can be fully understood by simply reading its file from top to bottom, without referencing oany other code or files. No base classes or common behaviour is factored out. This is a deliberate choice.
