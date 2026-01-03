SELECT
    r.name AS room_name
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) > 1;
