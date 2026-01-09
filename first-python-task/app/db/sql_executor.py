import os
from app.logger import logger


class SQLExecutor:
    def __init__(self, connection):
        self.connection = connection
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

    def _resolve_path(self, relative_path: str) -> str:
        return os.path.join(self.project_root, relative_path)

    def execute_script(self, relative_path: str):
        sql_path = self._resolve_path(relative_path)

        logger.info(f"Executing SQL script: {relative_path}")

        with open(sql_path, encoding="utf-8") as file:
            script = file.read()

        cursor = self.connection.cursor(buffered=True)

        try:
            for statement in script.split(';'):
                stmt = statement.strip()
                if stmt:  
                    cursor.execute(stmt)
                    #cursor.fetchall()
            
            self.connection.commit()
            logger.info(f"Executed SQL script: {relative_path}")
        
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error executing script {relative_path}: {e}")
            raise
        finally:
            cursor.close()

    def execute_select(self, relative_path: str) -> list[dict]:
            sql_path = self._resolve_path(relative_path)

            logger.info(f"Executing SELECT query: {relative_path}")

            with open(sql_path, encoding="utf-8") as file:
                sql = file.read().strip()

            cursor = self.connection.cursor(buffered=True, dictionary=True)  # dictionary=True — важно!

            try:
                cursor.execute(sql)
                results = cursor.fetchall()  # возвращаем все строки
                logger.info(f"SELECT completed: {relative_path}, fetched {len(results)} rows")
                return results
            except Exception as e:
                logger.error(f"Error executing SELECT {relative_path}: {e}")
                raise
            finally:
                cursor.close()

    def execute_many(self, relative_path: str, values: list[tuple]):
        sql_path = self._resolve_path(relative_path)

        logger.info(f"Executing batch SQL: {relative_path}")

        with open(sql_path, encoding="utf-8") as file:
            sql = file.read()

        cursor = self.connection.cursor()
        cursor.executemany(sql, values)
        self.connection.commit()
        cursor.close()

        logger.info(f"Batch insert completed: {relative_path}")

    def start_load(self, rooms_file: str, students_file: str) -> int:
        """
        Начинает новую загрузку и возвращает load_id
        """
        sql_path = "sql_queries/history/start_load.sql"
        sql = self._load_sql(sql_path)

        cursor = self.connection.cursor()
        cursor.execute(sql, (rooms_file, students_file))
        load_id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        
        logger.info(f"Started new load with load_id = {load_id}")
        return load_id

    def log_room_history(self, load_id: int, operation: str, room_id: int, room_name: str):
        sql_path = "sql_queries/history/log_room_history.sql"
        sql = self._load_sql(sql_path)

        cursor = self.connection.cursor()
        cursor.execute(sql, (load_id, operation, room_id, room_name))
        self.connection.commit()
        cursor.close()

    def log_student_history(self, load_id: int, operation: str, 
                            student_id: int, student_name: str, 
                            birthday, sex: str, room_id: int):
        sql_path = "sql_queries/history/log_student_history.sql"
        sql = self._load_sql(sql_path)

        cursor = self.connection.cursor()
        cursor.execute(sql, (load_id, operation, student_id, student_name, birthday, sex, room_id))
        self.connection.commit()
        cursor.close()

    def finish_load(self, load_id: int, status: str, stats: dict, error_message: str = None):
        sql_path = "sql_queries/history/finish_load.sql"
        sql = self._load_sql(sql_path)

        cursor = self.connection.cursor()
        cursor.execute(sql, (
            status,
            stats.get('rooms_inserted', 0),
            stats.get('rooms_updated', 0),
            stats.get('rooms_deleted', 0),
            stats.get('students_inserted', 0),
            stats.get('students_updated', 0),
            stats.get('students_deleted', 0),
            error_message or None,
            load_id
        ))
        self.connection.commit()
        cursor.close()
        
        logger.info(f"Load {load_id} finished with status: {status}")
    
    def _load_sql(self, relative_path: str) -> str:
        sql_path = self._resolve_path(relative_path)
        with open(sql_path, encoding="utf-8") as file:
            return file.read().strip()
        
    def execute_script_with_params(self, relative_path: str, params: tuple):
        sql = self._load_sql(relative_path)
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()
