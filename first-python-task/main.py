import os
from dotenv import load_dotenv

from app.cli import parse_args
from app.db.connection import DatabaseConnection
from app.db.schema import SchemaManager
from app.loaders.rooms_loader import RoomsLoader
from app.loaders.students_loader import StudentsLoader
from app.queries.room_queries import RoomQueries
from app.exporters.json_exporter import JsonExporter
from app.exporters.xml_exporter import XmlExporter

load_dotenv()


def main():
    args = parse_args()

    db = DatabaseConnection(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    conn = db.connect()

    schema = SchemaManager(conn)
    schema.create_tables()
    schema.create_indexes()
    schema.truncate_tables()

    RoomsLoader(conn, args.rooms).run()
    StudentsLoader(conn, args.students).run()

    queries = RoomQueries(conn)

    result = {
        "rooms_with_students_count": queries.rooms_with_students_count(),
        "top_5_rooms_with_smallest_avg_age": queries.top_5_rooms_with_smallest_avg(),
        "top_5_rooms_with_max_age_diff": queries.top_5_room_with_max_age_diff(),
        "rooms_with_mixed_sex": queries.rooms_with_mixed_sex(),
    }

    if args.format == "json":
        exporter = JsonExporter()
        output_file = "result.json"
    else:
        exporter = XmlExporter()
        output_file = "result.xml"

    exporter.export(result, output_file)

    conn.close()

    print(f"Results exported to {output_file}")

#python main.py --students students.json --rooms rooms.json --format json

if __name__ == "__main__":
    main()