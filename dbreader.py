import sqlite3

conn = sqlite3.connect('measurements.db')

data = conn.execute('SELECT * FROM measurements')

print(data.fetchall())

conn.close()
