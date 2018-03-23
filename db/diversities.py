import db as db
import warnings

def store(pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment, diversity):
    # cur.execute('INSERT INTO %s (day, elapsed_time, net_time, length, average_speed, geometry) VALUES (%s, %s, %s, %s, %s, %s)', (escaped_name, day, time_length, time_length_net, length_km, avg_speed, myLine_ppy))
    db.cursor.execute('INSERT INTO diversity (pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment, diversity) VALUES (%s, %s, %s, %s, %s, %s, %s)', (pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment, diversity))
    
def fetch(pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment):
    db.cursor.execute('SELECT diversity FROM diversity WHERE pso_name=%s AND swarm_size=%s AND benchmark_name=%s AND dimensionality=%s AND iteration=%s AND experiment=%s', (pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment))
    rows = db.cursor.fetchall()
    if len(rows) < 1:
        return None
    elif len(rows) > 1:
        warnings.warn("Multiple results found when looking diversities with {} {} {} {} {} {}".format(pso_name, swarm_size, benchmark_name, dimensionality, iteration, experiment))
        
    # rows is an array with an element for each returned row. We only expect one row (see warning above), so we take the first one.
    row = rows[0]
    
    # Each row is a tuple of columns. We only selected one column, so we take the first one.
    return row[0]
