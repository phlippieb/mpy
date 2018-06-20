from db import db
import warnings


def store(benchmark_name, dimensionality, step_size_fraction, experiment, g_avg, g_dev):
    db.cursor.execute(
        'INSERT INTO gradients (benchmark_name, dimensionality, step_size_fraction, experiment, g_avg, g_dev)' +
        'VALUES (%s, %s, %s, %s, %s, %s)' +
        'ON CONFLICT (benchmark_name, dimensionality, step_size_fraction, experiment)' +
        'DO UPDATE SET g_avg = %s, g_dev = %s',
        (benchmark_name, dimensionality, step_size_fraction, experiment, g_avg, g_dev, g_avg, g_dev))


def commit():
    db.connection.commit()


def fetch(benchmark_name, dimensionality, step_size_fraction, experiment):
    """Fetch and return g_avg and g_dev for the given identifiers."""
    db.cursor.execute(
        'SELECT g_avg, g_dev FROM gradients WHERE benchmark_name=%s AND dimensionality=%s AND step_size_fraction=%s AND experiment=%s',
        (benchmark_name, dimensionality, step_size_fraction, experiment))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when fetching gradients with benchmark_name={} and dimensionality={} and step_size_fraction={} and experiment={}".format(
            benchmark_name, dimensionality, step_size_fraction, experiment))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected two column, so we take those.
    return (row[0], row[1])
