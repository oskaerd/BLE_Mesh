import sqlite3

conn = sqlite3.connect('measurements.db')

data = conn.execute('SELECT * FROM measurements')

data = data.fetchall()

print(data)
print('Database stores ' + str(len(data)) + ' records.')

conn.close()
