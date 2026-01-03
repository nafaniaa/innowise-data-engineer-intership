import os
import json
from dotenv import load_dotenv
from dateutil import parser

from app.cli import parse_args
from app.logger import logger
from app.db.connection import DatabaseConnection
from app.db.sql_executor import SQLExecutor
from app.services.analytics_service import AnalyticsService
from app.exporters.json_exporter import JsonExporter
from app.exporters.xml_exporter import XmlExporter


load_dotenv()


def main():
    args = parse_args()

    # --- Database connection ---
    db = DatabaseConnection(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    conn = db.connect()
    logger.info("Database connection established")

    executor = SQLExecutor(conn)

    # --- DDL operations ---
    executor.execute_script("sql_queries/ddl/create_tables.sql")
    executor.execute_script("sql_queries/ddl/create_indexes.sql")
    executor.execute_script("sql_queries/ddl/truncate_tables.sql")

    # --- Load source data ---
    with open(args.rooms, encoding="utf-8") as f:
        rooms = json.load(f)

    room_values = [(room["id"], room["name"]) for room in rooms]
    executor.execute_many(
        "sql_queries/dml/insert_rooms.sql",
        room_values
    )
    logger.info("Rooms data loaded")

    with open(args.students, encoding="utf-8") as f:
        students = json.load(f)

    student_values = []
    for student in students:
        student_values.append(
            (
                student["id"],
                student["name"],
                parser.parse(student["birthday"]),
                student["sex"],
                student["room"]
            )
        )

    executor.execute_many(
        "sql_queries/dml/insert_students.sql",
        student_values
    )
    logger.info("Students data loaded")

    # --- Analytics ---
    analytics = AnalyticsService(executor)

    rooms_with_students = analytics.rooms_with_students_count()
    min_avg_age = analytics.top_5_rooms_with_smallest_avg_age()
    max_age_diff = analytics.top_5_rooms_with_max_age_diff()
    mixed_sex_rooms = analytics.rooms_with_mixed_sex()

    # --- Export results ---
    if args.format == "json":
        exporter = JsonExporter()
        extension = "json"
    else:
        exporter = XmlExporter()
        extension = "xml"

    exporter.export(
        rooms_with_students,
        f"results/rooms_with_students_count.{extension}"
    )
    exporter.export(
        min_avg_age,
        f"results/top_5_rooms_with_smallest_avg_age.{extension}"
    )
    exporter.export(
        max_age_diff,
        f"results/top_5_rooms_with_max_age_diff.{extension}"
    )
    exporter.export(
        mixed_sex_rooms,
        f"results/rooms_with_mixed_sex.{extension}"
    )

    logger.info("Analytics results exported")

    conn.close()
    logger.info("Database connection closed")


if __name__ == "__main__":
    main()

#python main.py --students src_data/students.json --rooms src_data/rooms.json --format json