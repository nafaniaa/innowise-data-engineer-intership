import mysql.connector
from mysql.connector import Error

class SchemaManager:
    def __init__(self, connection):
        self.connection = connection
    
    def create_tables(self):
        try:
            cursor = self.connection.cursor() 

            #room table
            cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS rooms(
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL                     
                ) ENGINE = InnoDB;
            """)

            #students table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                birthday DATETIME NOT NULL,
                sex CHAR(1) NOT NULL,
                room_id INT NOT NULL,
                CONSTRAINT fk_students_room
                    FOREIGN KEY (room_id)
                    REFERENCES rooms(id)
                    ON DELETE CASCADE           
            ) ENGINE = InnoDB;
            """)

            self.connection.commit()
            print("Таблицы успешно проверены/созданы.")
        except Error as e:
            print(f"Ошибка при создании таблиц: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
        


    def create_indexes(self):
            try:
                cursor = self.connection.cursor()
                indexes_to_create = {
                    "idx_students_room_id": "students(room_id)",
                    "idx_students_sex": "students(sex)",
                    "idx_students_birthday": "students(birthday)"
                }

                #проверка на существование индкса в базе
                for index_name, column in indexes_to_create.items():
                    check_query = f"""
                    SELECT COUNT(1) 
                    FROM information_schema.statistics 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'students' 
                    AND index_name = '{index_name}'
                    """

                    cursor.execute(check_query)
                    

                    result = cursor.fetchone()
                    if result and (result[0] if isinstance(result, tuple) else result['COUNT(1)']) == 0:
                        cursor.execute(f"CREATE INDEX {index_name} ON {column};")
                        print(f"Индекс {index_name} создан.")
                    else:
                        print(f"Индекс {index_name} уже существует, пропуск.")

                self.connection.commit()
            except Error as e:
                print(f"Ошибка при создании индексов: {e}")
                self.connection.rollback()
            finally:
                cursor.close()