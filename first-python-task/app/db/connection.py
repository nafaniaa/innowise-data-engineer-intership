import mysql.connector 

class DatabaseConnection:
    def __init__(self, host, port, database, user, password):
        self._config = { #сохраняет параметры в виде словаря
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password" : password,
        }
    
    def connect(self): #устанавливает реальное соединение с сервером
        return mysql.connector.connect(**self._config) # метод возввращает объект connection
    #через него можно отправлять sql запросы
    