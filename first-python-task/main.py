import os
import json
from dotenv import load_dotenv
from dateutil import parser

from app.cli import parse_args
from app.logger import logger
from app.db.connection import DatabaseConnection
from app.db.sql_executor import SQLExecutor
from app.services.analytics_service import AnalyticsService
from app.services.load_service import LoadService
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
    logger.info("Database connection established")

    executor = SQLExecutor(conn)

    executor.execute_script("sql_queries/ddl/create_tables.sql")
    executor.execute_script("sql_queries/ddl/create_indexes.sql")
    executor.execute_script("sql_queries/ddl/create_history_tables.sql")

    with open(args.rooms, encoding="utf-8") as f:
        rooms = json.load(f)

    with open(args.students, encoding="utf-8") as f:
        students = json.load(f)

    load_service = LoadService(executor)

    load_id = executor.start_load(args.rooms, args.students)

    try:
        rooms_stats = load_service.load_rooms_incremental(rooms, load_id)
        logger.info("Rooms loaded incrementally")

        student_values = []
        for student in students:
            student_values.append({
                "id": student["id"],
                "name": student["name"],
                "birthday": parser.parse(student["birthday"]),
                "sex": student["sex"],
                "room": student["room"]
            })

        students_stats = load_service.load_students_incremental(student_values, load_id)
        logger.info("Students loaded incrementally")

        executor.finish_load(load_id, "SUCCESS", {**rooms_stats, **students_stats})

    except Exception as e:
        executor.finish_load(load_id, "FAILED", {}, str(e))
        logger.error(f"Load failed: {e}")
        raise

    analytics = AnalyticsService(executor)

    rooms_with_students = analytics.rooms_with_students_count()
    min_avg_age = analytics.top_5_rooms_with_smallest_avg_age()
    max_age_diff = analytics.top_5_rooms_with_max_age_diff()
    mixed_sex_rooms = analytics.rooms_with_mixed_sex()

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