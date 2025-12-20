import mysql.connector

class DatabaseConnection:
    def __init__(self, host, port, database, user, password):
        self._config = { 
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

    def connect(self):
        return mysql.connector.connect(**self._config)
