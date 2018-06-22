# TODO: this might be better suited to live inside psodroc.pso

from psodroc.pso import alternative_barebones_pso, \
    barebones_pso, \
    gbest_pso, \
    gc_gbest_pso, \
    gc_lbest_pso, \
    gc_von_neumann_pso, \
    lbest_pso, \
    social_only_pso, \
    von_neumann_pso


def get(name):
    if name == 'alternative_barebones_pso':
        return alternative_barebones_pso
    elif name == 'barebones_pso':
        return barebones_pso
    elif name == 'gbest_pso':
        return gbest_pso
    elif name == 'gc_gbest_pso':
        return gc_gbest_pso
    elif name == 'gc_lbest_pso':
        return gc_lbest_pso
    elif name == 'gc_von_neumann_pso':
        return gc_von_neumann_pso
    elif name == 'lbest_pso':
        return lbest_pso
    elif name == 'social_only_pso':
        return social_only_pso
    elif name == 'von_neumann_pso':
        return von_neumann_pso
    else:
        raise Exception("Unrecognized PSO name {}".format(name))


all_names = [
    'alternative_barebones_pso',
    'barebones_pso',
    'gbest_pso',
    'gc_gbest_pso',
    'gc_lbest_pso',
    'gc_von_neumann_pso',
    'lbest_pso',
    'social_only_pso',
    'von_neumann_pso'
]
