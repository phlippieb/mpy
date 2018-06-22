def norm(xs, min_in=0., max_in=1., min_out=0., max_out=1.):
    """Normalise xs from the input range to the output range."""
    range_in = max_in - min_in
    range_out = max_out - min_out
    a = (max_out - min_out) / (max_in - min_in)
    b = max_out - (a * max_in)
    return [a * x + b for x in xs]
