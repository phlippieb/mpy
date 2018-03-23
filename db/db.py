import psycopg2

connection = psycopg2.connect("dbname='psodroc' user='phlippieb' host='localhost'")# password='dbpass'")
connection.set_session(autocommit=True)
cursor = connection.cursor()



