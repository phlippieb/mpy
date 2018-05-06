from scipy import optimize
import numpy as np
        
# A Two-piecewise linear approximation.
# The approximation is represented in a format that fascilitates fixing the y-value at x=0.
class TwoPiecewiseLinearApproximation:
    # The y-coordinate at x=0
    y0 = 0
    
    # The slope of the first line, which ends at the breakpoint:
    m1 = 0
    
    # The x-coordinate at the breakpoint:
    x1 = 0
    
    # The slope of the second line, which starts at the breakpoint:
    m2 = 0
    
    # Initialize the object's properties directly
    def __init__(self, y0, m1, x1, m2):
        self.y0 = y0
        self.m1 = m1
        self.x1 = x1
        self.m2 = m2

# Given x- and y-values of a set of data, fit a two-piecewise linear approximation to the data.
def fit_to(xs, ys):
    # Ensure that xs are floats:
    xs = [float(x) for x in xs]
    
    # Bound the parameters of _2pwl as follows:
    # - m1 (the slope of the first line) is expected to be between 0 and -inf
    # - x2 (the breakpoint x value) is between 0 and the max x
    # - m2 (the slope of the second line) is expected to be between 0 and -inf, but it could go above 0, and is left unbounded
    bounds = ([-np.inf, 0, -np.inf], [0, max(xs), np.inf])

    # Estimate that the breakpoint will be halway along the x-axis,
    # that the first line's slope will be -2 (slightly steeper than a 45 degree angle).
    # and that the second line's slope will be -0.5 (slightly shallower than a 45 degree angle).
    p0 = [-2, max(xs)/2, -0.5]

    # Optimize a two-piecewise linear approximation of the given data.
    # optimal_params will be the [m1, x2, m2] that yield the optimal linear approximation of the given data.
    # error is ignored.
    # optimal_params, error = optimize.curve_fit(_2pwl, xs, ys, bounds=bounds, p0=p0)
    y0 = ys[0]
    q = get_2pwl(ys[0])
    optimal_params, error = optimize.curve_fit(q, xs, ys, bounds=bounds, p0=p0)

    # Return the result as a TwoPiecewiseLinearApproximation object
    # return TwoPiecewiseLinearApproximation_old(optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3])
    return TwoPiecewiseLinearApproximation(y0=y0, m1=optimal_params[0], x1=optimal_params[1], m2=optimal_params[2])

# Plot a given two-piecewise linear function between 0 and the given maxX.
# TODO: fix this function to use new representation
# def plot(maxX, tpwla):
#     xs = np.linspace(0, maxX, maxX)
#     import matplotlib.pyplot as plt
#     plt.plot(xs, _2pwl(xs, tpwla.x, tpwla.y, tpwla.m1, tpwla.m2), color="black")

# This function returns a piecewise object.
# y1: The y-value at x=0
# m1: The slope of the first line
# x2: The x-value at the breakpoint
# m2: The slope of the second line
def _2pwl(x, y0, m1, x2, m2):
    return np.piecewise(x,
        condlist=[x<x2],
        funclist=[
            lambda x: m1*x + y0,
            lambda x: m2*(x + x2) + (m1*x2 + y0)
        ])

# Partially apply the given y0 to _2pwl in order to fix the starting value (at x=0) of the piecewise object to the given y-value.
def get_2pwl(y0):
    def _2pwl(x, m1, x2, m2):
        return np.piecewise(x,
            condlist=[x<x2],
            funclist=[
                lambda x: m1*x + y0,
                lambda x: m2*(x + x2) + (m1*x2 + y0)
            ])
    return _2pwl
