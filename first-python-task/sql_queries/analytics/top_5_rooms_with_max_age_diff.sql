SELECT
    r.name AS room_name,
    MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) -
    MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS diff_age
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
ORDER BY diff_age DESC
LIMIT 5;
