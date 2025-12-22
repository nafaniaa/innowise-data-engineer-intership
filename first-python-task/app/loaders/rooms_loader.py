from app.loaders.base_loader import BaseLoader

class RoomsLoader(BaseLoader):
    def insert(self, data: list):
        cursor = self.connection.cursor()

        query = """
        INSERT INTO rooms(id, name) 
        VALUES (%s, %s)
        """

        values = [(room["id"], room["name"]) for room in data]

        cursor.executemany(query, values)
        self.connection.commit()
        cursor.close()