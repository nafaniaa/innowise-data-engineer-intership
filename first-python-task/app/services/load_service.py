from app.logger import logger

class LoadService:
    def __init__(self, executor):
        self.executor = executor

    def load_rooms_incremental(self, new_rooms: list[dict], load_id: int) -> dict:
        # 1. 
        current_rooms = self.executor.execute_select("sql_queries/dml/select_all_rooms.sql")
        current_dict = {room["id"]: room["name"] for room in current_rooms}
        new_dict = {room["id"]: room["name"] for room in new_rooms}

        stats = {"rooms_inserted": 0, "rooms_updated": 0, "rooms_deleted": 0}

        # 2. INSERT и UPDATE
        for room in new_rooms:
            room_id = room["id"]
            room_name = room["name"]

            if room_id not in current_dict:
                self.executor.execute_script_with_params(
                    "sql_queries/dml/insert_room.sql", (room_id, room_name)
                )
                self.executor.log_room_history(load_id, "INSERT", room_id, room_name)
                stats["rooms_inserted"] += 1
                logger.info(f"Inserted room id={room_id}")
            elif current_dict[room_id] != room_name:
                self.executor.execute_script_with_params(
                    "sql_queries/dml/update_room.sql", (room_name, room_id)
                )
                self.executor.log_room_history(load_id, "UPDATE", room_id, room_name)
                stats["rooms_updated"] += 1
                logger.info(f"Updated room id={room_id}")

        # 3. DELETE
        for room_id in current_dict.keys() - new_dict.keys():
            old_name = current_dict[room_id]
            self.executor.execute_script_with_params(
                "sql_queries/dml/delete_room.sql", (room_id,)
            )
            self.executor.log_room_history(load_id, "DELETE", room_id, old_name)
            stats["rooms_deleted"] += 1
            logger.info(f"Deleted room id={room_id}")

        return stats
    
    def load_students_incremental(self, new_students: list[dict], load_id: int) -> dict:
        current_students = self.executor.execute_select("sql_queries/dml/select_all_students.sql")
        
        current_dict = {
            s["id"]: (s["name"], s["birthday"].date() if s["birthday"] else None, s["sex"], s["room_id"])
            for s in current_students
        }

        new_ids = set()
        stats = {"students_inserted": 0, "students_updated": 0, "students_deleted": 0}

        for student in new_students:
            stud_id = student["id"]
            name = student["name"]
            birthday = student["birthday"]
            sex = student["sex"]
            room_id = student["room"]

            new_ids.add(stud_id)

            current_tuple = current_dict.get(stud_id)

            if current_tuple is None:
                self.executor.execute_script_with_params(
                    "sql_queries/dml/insert_student.sql",
                    (stud_id, name, birthday, sex, room_id)
                )
                self.executor.log_student_history(load_id, "INSERT", stud_id, name, birthday, sex, room_id)
                stats["students_inserted"] += 1
                logger.info(f"Inserted student id={stud_id}")

            elif current_tuple != (name, birthday.date(), sex, room_id):
                self.executor.execute_script_with_params(
                    "sql_queries/dml/update_student.sql",
                    (name, birthday, sex, room_id, stud_id)
                )
                self.executor.log_student_history(load_id, "UPDATE", stud_id, name, birthday, sex, room_id)
                stats["students_updated"] += 1
                logger.info(f"Updated student id={stud_id}")

        for stud_id in set(current_dict.keys()) - new_ids:
            # Находим старые данные для логирования
            old_student = next(s for s in current_students if s["id"] == stud_id)
            self.executor.execute_script_with_params(
                "sql_queries/dml/delete_student.sql", (stud_id,)
            )
            self.executor.log_student_history(
                load_id, "DELETE", stud_id,
                old_student["name"], old_student["birthday"], old_student["sex"], old_student["room_id"]
            )
            stats["students_deleted"] += 1
            logger.info(f"Deleted student id={stud_id}")

        return stats