import sqlite3

db_select_query = 'SELECT * FROM measurements'
db_count_query='SELECT count(*) FROM measurements'

conn = sqlite3.connect('measurements.db')

data = conn.execute(db_select_query)

data = data.fetchall()
print(data)
records = conn.execute(db_count_query).fetchall()[0][0]
print('Database stores ' + str(records) + ' records.')

print(conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())

conn.close()
