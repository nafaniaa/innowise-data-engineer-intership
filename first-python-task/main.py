import os
from dotenv import load_dotenv
from app.db.connection import DatabaseConnection
from app.db.schema import SchemaManager
from app.loaders.rooms_loader import RoomsLoader
from app.loaders.students_loader import StudentsLoader

load_dotenv()

def main():
    db = DatabaseConnection(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    try:
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT 1 AS test;")
        print(cursor.fetchone())
        schema = SchemaManager(conn)
        schema.create_tables()
        schema.create_indexes()
        cursor.close()

        RoomsLoader(conn, "rooms.json").run()
        StudentsLoader(conn, "students.json").run()

        conn.close()
    except Exception as e:
        print(f"Ошибка: {e}")    


if __name__ == "__main__":
    main()