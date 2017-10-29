from scipy import optimize
import numpy as np

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
    
# Given the x- and y-values of a set of data, this function returns a two-piecewise linear approximation of the data.
def getTwoPiecewiseLinearApproximation(xs, ys):
    p, e = optimize.curve_fit(_pwl, xs, ys)
    result = TwoPiecewiseLinearApproximation()
    result.x = p[0]
    result.y = p[1]
    result.m1 = p[2]
    result.m2 = p[3]
    return result


# Helper method that's passed to an optimization method.
def _pwl(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

