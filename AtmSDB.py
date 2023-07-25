import mysql.connector
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Omi@2005",
            database="atmdatabase"
        )

    def execute_query(self, query, values=None):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def fetch_query(self, query, values=None):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all_query(self, query, values=None):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
