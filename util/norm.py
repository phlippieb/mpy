def norm(xs, in_low=0., in_high=1., out_low=0., out_high=1.):
    """Map each element in xs from the range [in_low, in_high] to the range [out_low, out_high]."""
    in_range = in_high - in_low
    out_range = out_high - out_low
    return [(x - in_low) * (out_range / in_range) + out_low for x in xs]
