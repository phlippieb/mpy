from db import db
import warnings


def store(benchmark_name, dimensionality, experiment, measurement):
    db.cursor.execute(
        'INSERT INTO DM_OLD (benchmark_name, dimensionality, experiment, measurement)' +
        'VALUES (%s, %s, %s, %s)' +
        'ON CONFLICT (benchmark_name, dimensionality, experiment)' +
        'DO UPDATE SET measurement = %s',
        (benchmark_name, dimensionality, experiment, measurement, measurement))


def commit():
    db.connection.commit()


def fetch(benchmark_name, dimensionality, experiment):
    db.cursor.execute(
        'SELECT measurement FROM DM_OLD WHERE benchmark_name=%s AND dimensionality=%s AND experiment=%s',
        (benchmark_name, dimensionality, experiment))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when fetching DM with benchmark_name={} and dimensionality={} and experiment={}".format(
            benchmark_name, dimensionality, experiment))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
