class RoomQueries():
    def __init__(self, connection):
        self.connection = connection

    #List of rooms and the number of students in each of them
    def  rooms_with_students_count(self):
        cursor = self.connection.cursor(dictionary=True)  

        query = """
          SELECT r.name AS room_name,
          COUNT(s.id) AS students_count
          FROM rooms r
          LEFT JOIN students s ON s.room_id = r.id
          GROUP BY r.id, r.name;
          """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    
    #5 rooms with the smallest average age of students
    def top_5_rooms_with_smallest_avg(self):
        cursor = self.connection.cursor(dictionary = True)

        query = """ 
        SELECT r.name AS room_name,
        AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
        FROM rooms r
        JOIN students s ON s.room_id = r.id
        GROUP BY r.id, r.name
        ORDER BY avg_age ASC
        LIMIT 5;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    
    #5 rooms with the largest difference in the age of students
    def top_5_room_with_max_age_diff(self):
        cursor = self.connection.cursor(dictionary = True)

        query = """SELECT r.name AS room_name,
        MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) -
        MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS diff_age
        FROM rooms r
        JOIN students s ON s.room_id = r.id
        GROUP BY r.id, r.name
        ORDER BY diff_age DESC
        LIMIT 5;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    #List of rooms where different-sex students live
    def rooms_with_mixed_sex(self):
        cursor = self.connection.cursor(dictionary = True)

        query = """SELECT r.name AS room_name
        FROM rooms r
        JOIN students s ON s.room_id = r.id
        GROUP BY r.id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result