import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82–102, July 1999.

def goldstein_price(x1, x2):
    a1 = np.square(x1 + x2 + 1)
    a2 = 19 - (14 * x1) + (3 * np.square(x2)) - (14 * x2) + (6 * x1 * x2) + (3 * np.square(x2))
    a = 1 + (a1 * a2)
    b1 = np.square((2 * x1) - (3 * x2))
    b2 = 18 - (32 * x1) + (12 * np.square(x1)) + (48 * x2) - (36 * x1 * x2) + (27 * np.square(x2))
    b = 30 + (b1 * b2)
    return a * b

domain = [-2, 2]
# min = [0, -1] = 3
