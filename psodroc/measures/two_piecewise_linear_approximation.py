from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

# A structure to hold the result of a two-piecewise linear approximation calculation.
# A two-piecewise linear approximation consist of two straight lines that meet at a breakpoint.
# Each line is an approximation of some data that yields the least error.
class TwoPiecewiseLinearApproximation:
    # The x-coordinate of the breakpoint
    x = 0

    # The y-coordinate of the breakpoint
    y = 0

    # The slope of the first line, which ends at the breakpoint
    m1 = 0

    # The slope of the second line, which starts at the breakpoint.
    m2 = 0

    def __init__(self, x, y, m1, m2):
        self.x = x
        self.y = y
        self.m1 = m1
        self.m2 = m2

# Given x- and y-values of a set of data, fit a two-piecewise linear approximation to the data.
def fit_to(xs, ys):
    # Ensure that xs are floats:
    xs = [float(x) for x in xs]

    # Bound the parameters of _2pwl as follows:
    # - x0 (the breakpoint x value) is between 0 and the max x
    # - y0 (the breakpoint y value) is between 0 and the max y
    # - m1 (the slope of the first line) is expected to be between 0 and -inf (though it might go above 0 in some cases, so we leave it unbounded)
    # - Ditto for m2 (the slope of the second line)
    bounds = ([0, 0, -np.inf, -np.inf], [max(xs), max(ys), np.inf, np.inf])

    # Estimate that the breakpoint between the lines will be halfway down max(xs),
    # that the first line's slope will be -2 (slightly steeper than a 45 degree angle).
    # and that the second line's slope will be -0.5 (slightly shallower than a 45 degree angle).
    p0 = [max(xs)/2, ys[int(max(xs))/2], -2, -0.5]

    # Optimize a two-piecewise linear approximation of the given data.
    # optimal_params will be the [x0, y0, m1, m2] that yield the optimal linear approximation of the given data.
    # error is ignored.
    optimal_params, error = optimize.curve_fit(_2pwl, xs, ys, bounds=bounds, p0=p0)

    # Return the result as a TwoPiecewiseLinearApproximation object
    return TwoPiecewiseLinearApproximation(optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3])

# Plot a given two-piecewise linear function between 0 and the given maxX.
def plot(maxX, tpwla):
    xs = np.linspace(0, maxX, maxX)
    plt.plot(xs, _2pwl(xs, tpwla.x, tpwla.y, tpwla.m1, tpwla.m2), color="black")

# This function gives two lines with the given slopes that break at the given coordinates.
# When fitting a piecewise approximation on some data, the error between the data and this function are minimized.
# Also used to plot a piecewise approximation.
# x0: the x-coordinate of the breakpoint between the two lines
# y0: the y-coordinate of the breakpoint between the two lines
# k1: the slope of the first line
# k2: the slope of the second line
def _2pwl(x, x0, y0, m1, m2):
    return np.piecewise(x, condlist=[x < x0], funclist=[lambda x: m1*x + y0 - m1*x0, lambda x: m2*x + y0 - m2*x0])
