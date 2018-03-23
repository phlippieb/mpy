import results.diversities as diversities
import results.drocs as drocs
import db.db

x = diversities.get('gbest_pso', 5, 'spherical', 2, 0, 0)
print(x)    
