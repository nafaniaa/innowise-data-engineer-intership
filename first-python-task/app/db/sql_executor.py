import os
from app.logger import logger


class SQLExecutor:
    def __init__(self, connection):
        self.connection = connection

        # project root = .../first-python-task
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

    def _resolve_path(self, relative_path: str) -> str:
        """
        Resolve SQL file path relative to project root
        """
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
            """
            Execute a SELECT query from file and return results as list of dicts
            """
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
