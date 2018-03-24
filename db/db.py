import psycopg2

print 'getting db connection...'
connection = psycopg2.connect("dbname='psodroc' user='phlippieb' host='localhost'")# password='dbpass'")
connection.set_session(autocommit=True)
print 'getting db cursor...'
cursor = connection.cursor()
print 'db ready.'



