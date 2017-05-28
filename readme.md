# About
This is a library that provides PSO algorithms, optimisation benchmark functions, and stuff that measures several properties of both. I am writing this to perform experiments for my master's thesis on links between diversity rate-of-change of PSOs and the fitness landscape characteristics of the objective functions that they optimise.

## Structure
The `psodroc` package contains modules for PSO algorithms under `pso` and benchmark functions under `benchmark`. The project root contains an example script that runs the algorithms.

Each benchmark is in a file called `<benchmark name>.py`. In each benchmark file, the actual function implementation is in a function called `function(xs)`, which takes a candidate solution vector as a parameter. Each file also provides the benchmark's domain through functions called `min(d)` and `max(d)`, which respectively return the minimum and maximum allowed `x` value in dimension `d`.

# Install
This library uses python 2.7 and `numpy`. Additionally, to explore and plot data, I recommend using `jupyter` notebooks and `matplotlib.pyplot`. The easiest way to get all of that is to install [miniconda](http://conda.pydata.org/miniconda.html), and then use the conda package manager to install components: `conda install numpy jupyter matplotlib`.

# Coding style
Instead of aiming to create an elegant, generic, extensible library, I opted to make the code straight-forward and clear. My chosen approach can be summed up as "clarity over elegance". This especially caused me to reject DRY (don't repeat yourself) in favour of defining each algorithm, benchmark and measurement as an independent script. There will be lots of repeated code, but any part of the library can be fully understood by simply reading its file from top to bottom, without referencing oany other code or files. No base classes or common behaviour is factored out. This is a deliberate choice.

# TODO
Check out this link on piecewise linear approximation in numpy/scipy and implement my DRoC measure in python:
http://stackoverflow.com/questions/29382903/how-to-apply-piecewise-linear-fit-in-python

Structure project according to this guideline:
https://python-packaging.readthedocs.io/en/latest/minimal.html
