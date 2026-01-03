SELECT
    r.name AS room_name,
    COUNT(s.id) AS students_count
FROM rooms r
LEFT JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name;
