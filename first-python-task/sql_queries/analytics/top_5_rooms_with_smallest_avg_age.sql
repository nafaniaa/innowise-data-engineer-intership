SELECT
    r.name AS room_name,
    AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
ORDER BY avg_age ASC
LIMIT 5;
