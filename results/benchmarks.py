# TODO might be better suited to live in psodroc.benchmarks

from psodroc.benchmarks import ackley, \
    alpine, \
    beale, \
    bohachevsky1_generalized, \
    eggholder, \
    goldstein_price, \
    griewank, \
    levy13_generalized, \
    michalewicz, \
    pathological, \
    quadric, \
    quartic, \
    rastrigin, \
    rosenbrock, \
    salomon, \
    schwefel_2_22, \
    schwefel_2_26, \
    six_hump_camel_back, \
    skew_rastrigin, \
    spherical, \
    step, \
    weierstrass, \
    zakharov


def get(name):
    if name == 'ackley':
        return ackley
    elif name == 'alpine':
        return alpine
    elif name == 'beale':
        return beale
    elif name == 'bohachevsky1_generalized':
        return bohachevsky1_generalized
    elif name == 'eggholder':
        return eggholder
    elif name == 'goldstein_price':
        return goldstein_price
    elif name == 'griewank':
        return griewank
    elif name == 'levy13_generalized':
        return levy13_generalized
    elif name == 'michalewicz':
        return michalewicz
    elif name == 'pathological':
        return pathological
    elif name == 'quadric':
        return quadric
    elif name == 'quartic':
        return quartic
    elif name == 'rastrigin':
        return rastrigin
    elif name == 'rosenbrock':
        return rosenbrock
    elif name == 'salomon':
        return salomon
    elif name == 'schwefel_2_22':
        return schwefel_2_22
    elif name == 'schwefel_2_26':
        return schwefel_2_26
    elif name == 'six_hump_camel_back':
        return six_hump_camel_back
    elif name == 'skew_rastrigin':
        return skew_rastrigin
    elif name == 'spherical':
        return spherical
    elif name == 'step':
        return step
    elif name == 'weierstrass':
        return weierstrass
    elif name == 'zakharov':
        return zakharov
    else:
        raise Exception('Unrecognized benchmark {}'.format(name))


all_names = [
    'ackley',
    'alpine',
    'beale',
    'bohachevsky1_generalized',
    'eggholder',
    'goldstein_price',
    'griewank',
    'levy13_generalized',
    'michalewicz',
    'pathological',
    'quadric',
    'quartic',
    'rastrigin',
    'rosenbrock',
    'salomon',
    'schwefel_2_22',
    'schwefel_2_26',
    'six_hump_camel_back',
    'skew_rastrigin',
    'spherical',
    'step',
    'weierstrass',
    'zakharov'
]
