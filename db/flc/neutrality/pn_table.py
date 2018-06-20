from db import db
import warnings


def store(benchmark_name, dimensionality, epsilon, experiment, measurement):
    db.cursor.execute(
        'INSERT INTO PN (benchmark_name, dimensionality, epsilon, experiment, measurement)' +
        'VALUES (%s, %s, %s, %s, %s)' +
        'ON CONFLICT (benchmark_name, dimensionality, epsilon, experiment)' +
        'DO UPDATE SET measurement = %s',
        (benchmark_name, dimensionality, epsilon, experiment, measurement, measurement))


def commit():
    db.connection.commit()


def fetch(benchmark_name, dimensionality, epsilon, experiment):
    db.cursor.execute(
        'SELECT measurement FROM PN WHERE benchmark_name=%s AND dimensionality=%s AND epsilon=%s AND experiment=%s',
        (benchmark_name, dimensionality, epsilon, experiment))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when fetching PN with benchmark_name={} and dimensionality={} and epsilon={} and experiment={}".format(
            benchmark_name, dimensionality, epsilon, experiment))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
