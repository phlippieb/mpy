import db as db
import warnings

def store(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, result):
    db.cursor.execute(
        'INSERT INTO droc (pso_name, swarm_size, benchmark_name, dimensionality, iterations, experiment, droc)' +
        'VALUES (%s, %s, %s, %s, %s, %s, %s)' +
        'ON CONFLICT (pso_name, swarm_size, benchmark_name, dimensionality, iterations, experiment)' +
        'DO UPDATE SET droc = %s',
        (pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, result, result))

def commit():
    db.connection.commit()

def fetch(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num):
    db.cursor.execute(
        'SELECT droc FROM droc WHERE pso_name=%s AND swarm_size=%s AND benchmark_name=%s AND dimensionality=%s AND iterations=%s AND experiment=%s',
        (pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when looking for droc with {} {} {} {} {} {}".format(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
