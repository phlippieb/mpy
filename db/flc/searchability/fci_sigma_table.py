from db import db
import warnings


def store(benchmark_name, dimensionality, measurement):
    db.cursor.execute(
        'INSERT INTO FCI_sigma (benchmark_name, dimensionality, fci_sigma)' +
        'VALUES (%s, %s, %s)' +
        'ON CONFLICT (benchmark_name, dimensionality)' +
        'DO UPDATE SET fci_sigma = %s',
        (benchmark_name, dimensionality, measurement, measurement))


def commit():
    db.connection.commit()


def fetch(benchmark_name, dimensionality):
    db.cursor.execute(
        'SELECT fci_sigma FROM FCI_sigma WHERE benchmark_name=%s AND dimensionality=%s',
        (benchmark_name, dimensionality))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when fetching FCI_sigma with benchmark_name={} and dimensionality={}".format(
            benchmark_name, dimensionality))

    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]

    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
