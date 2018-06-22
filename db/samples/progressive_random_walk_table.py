from db import db
import numpy as np
import warnings
from psodroc.measures import progressive_random_walk
from util import norm
import sys


def get(
        dimensionality,
        step_size_fraction,
        starting_zone_num,
        num_steps,
        experiment,
        domain_min,
        domain_max):
    """Return the steps from a particular walk.

    Attempt to fetch all the steps from the DB.
    If any are missing, calculate the entire walk and store it for future queries.

    Args:
        dimensionality: Int. The number of dimensions of the sampled search space.
        step_size_fraction: Float. The max step size as a fraction of the domain; i.e. in [0, 1].
        starting_zone_num: Int. When performing multiple walks, the number of starting zones should equal the number of dimensions. Which starting zone is this?
        num_steps: Int. How many steps are required.
        experiment: Multiple 'experiments' or samples of groups of walks are supported.
        domain_min, domain_max: The domain range to convert the walk to.

    Returns:
        Array: num_steps x dimensions x Float. An array of steps, each of which is a vector of dimensional position components.
    """
    # Try to fetch all requested steps.
    steps = np.zeros([num_steps, dimensionality])
    is_complete = True
    last_percent = 0
    print '\r[walk db] Fetching existing steps (', last_percent, 'percent )...\r',
    sys.stdout.flush()
    for step in range(num_steps):
        percent = int(((step+1) * 100.) / num_steps)
        if percent > (last_percent):
            print '\r[walk db] Fetching existing steps (', percent, 'percent )...\r',
            sys.stdout.flush()
            last_percent = percent

        # for dimension in range(dimensionality):
            # component = fetch_component(
            #     dimensionality,
            #     step_size_fraction,
            #     starting_zone_num,
            #     experiment,
            #     step,
            #     dimension)

            # if component is None:
            #     # There is missing data! We need to (re-)calculate.
            #     is_complete = False
            #     break

            # steps[step][dimension] = component

        step_data = fetch_step(
            dimensionality,
            step_size_fraction,
            starting_zone_num,
            experiment,
            step)

        if step_data is None:
            # There is missing data! We need to (re-)calculate.
            is_complete = False
            break

        for dimension in range(dimensionality):
            steps[step][dimension] = step_data[dimension]
    print ''

    if is_complete:
        # All data was found in the DB.
        # Convert the steps to the requested domain bounds.
        print '[walk db] All steps found. Returning.'
        steps = norm.norm(steps, 0., 1., domain_min, domain_max)
        return steps

    # Else: not all data was found. (Re-)calculate.
    print '[walk db] All steps NOT found. Calculating....'
    starting_zones = progressive_random_walk.get_starting_zones(dimensionality)
    starting_zone = starting_zones[starting_zone_num]
    steps = progressive_random_walk.walk(
        dimensionality, 0., 1., num_steps, step_size_fraction, starting_zone)

    # Store the result for future queries.
    last_percent = 0
    print '\r[walk db] Storing (', last_percent, 'percent )...\r',
    sys.stdout.flush()
    for (i, step) in enumerate(steps):
        percent = int(((i+1) * 100.) / num_steps)
        if percent > (last_percent):
            print '\r[walk db] Storing (', percent, 'percent )...\r',
            sys.stdout.flush()
            last_percent = percent

        for (j, component) in enumerate(step):
            store(dimensionality, step_size_fraction,
                  starting_zone_num, experiment, i, j, component)

    print ''
    commit()

    # Convert the steps to the requested domain bounds.
    print '[walk db] Denormalizing...'
    steps = norm.norm(steps, 0., 1., domain_min, domain_max)

    print '[walk db] Done.'
    return steps


def store(dimensionality, step_size, starting_zone, experiment, step, dimension, component):
    """Store a dimensional component of a step of a random walk."""
    db.cursor.execute(
        'INSERT INTO progressive_random_walk_step_component' +
        '(dimensionality, step_size, starting_zone, experiment, step, dimension, component)' +
        'VALUES (%s, %s, %s, %s, %s, %s, %s)' +
        'ON CONFLICT (dimensionality, step_size, starting_zone, step, dimension)' +
        'DO UPDATE SET component=%s',
        (dimensionality, step_size, starting_zone,
         experiment, step, dimension, component, component)
    )


def commit():
    db.connection.commit()


def fetch_component(dimensionality, step_size, starting_zone, experiment, step, dimension):
    """Fetch a dimensional component of a step of a random walk."""
    db.cursor.execute(
        'SELECT component FROM progressive_random_walk_step_component ' +
        'WHERE dimensionality = %s AND step_size = %s AND starting_zone = %s AND experiment = %s AND step = %s AND dimension = %s',
        (dimensionality, step_size, starting_zone, experiment, step, dimension)
    )

    rows = db.cursor.fetchall()

    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn(
            'Multiple results found when fetching progressive random walk component' +
            'dimensionality={} AND step_size={} AND starting_zone={} AND step={} AND dimension={}'
            .format(dimensionality, step_size, starting_zone, step, dimension))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected two column, so we take those.
    return row[0]


def fetch_step(dimensionality, step_size, starting_zone, experiment, step):
    """Fetch a step of a random walk."""
    db.cursor.execute(
        'SELECT component FROM progressive_random_walk_step_component ' +
        'WHERE dimensionality = %s AND step_size = %s AND starting_zone = %s AND experiment = %s AND step = %s ' +
        'ORDER BY dimension',
        (dimensionality, step_size, starting_zone, experiment, step)
    )

    rows = db.cursor.fetchall()

    if len(rows) != dimensionality:
        return None

    return [row[0] for row in rows]
