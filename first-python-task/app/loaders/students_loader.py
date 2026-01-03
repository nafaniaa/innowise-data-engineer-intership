from app.loaders.base_loader import BaseLoader
from dateutil import parser


class StudentsLoader(BaseLoader):
    def insert(self, data: list):
        cursor = self.connection.cursor()

        query = """
        INSERT INTO students (id, name, birthday, sex, room_id)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = []
        for student in data:
            birthday = parser.parse(student["birthday"]) #DATETIME
            values.append(
                (
                    student["id"],
                    student["name"],
                    birthday,
                    student["sex"],
                    student["room"]
                )
            )

        cursor.executemany(query, values)
        self.connection.commit()
        cursor.close()
