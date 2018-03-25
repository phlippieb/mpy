import db as db
import warnings

# Note: the order of PSOs matters

def store(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, rank):
    db.cursor.execute(
        'INSERT INTO droc_rank_between_psos (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, iterations, rank_value) ' +
        'VALUES (%s, %s, %s, %s, %s, %s, %s) ' +
        'ON CONFLICT (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, iterations) ' +
        'DO UPDATE SET rank_value = %s ',
        (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, rank, rank))
    
def fetch(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations):
    db.cursor.execute(
        'SELECT rank_value FROM droc_rank_between_psos ' +
        'WHERE pso_1_name = %s AND pso_2_name = %s ' +
        'AND swarm_size = %s AND benchmark_name = %s AND dimensionality = %s AND iterations = %s ',
        (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when looking for droc_rank_between_psos with {} {} {} {} {} {}".format(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations))
    
    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]
    
    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
        