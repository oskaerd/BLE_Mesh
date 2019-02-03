import sqlite3

database_filename = 'measurements.db'
db_read_query_head = 'SELECT *'
db_read_values = 'dev_id, temp, humidity, pressure, lux, battery)'
db_read_query_tail = ' from measurements'
db_create_table_cmd = 'CREATE TABLE measurements \
                (dev_id integer, temp real, humidity real, pressure real, \
                lux real, battery integer)'
db_insert_query = 'INSERT INTO measurements VALUES ('
db_count_query='SELECT count(*) FROM measurements'

samplesToDisplay = 20

class database_interface:
    def __init__(self):
        self.db_conn = sqlite3.connect(database_filename)

    def commit(self):
        self.db_conn.commit()

    def getData(self):
        self.graph_data = self.db_conn.execute(db_read_query_head + db_read_query_tail)
        self.graph_data = self.graph_data.fetchall()
        return self.graph_data

    def newTable(self, table_name):
        self.db_conn.execute(db_create_table_cmd)

    def writeData(self, query):
        records = self.getNumberOfRecords()
        self.db_conn.execute(query)
        if records > samplesToDisplay:
            self.db_conn.execute('DELETE FROM measurements WHERE ROWID IN \
                (SELECT ROWID FROM measurements ORDER BY ROWID DESC LIMIT -1 OFFSET 21)')

    def getNumberOfRecords(self):
        return self.db_conn.execute(db_count_query).fetchall()[0][0]

    def closeConn(self):
        self.db_conn.close()
