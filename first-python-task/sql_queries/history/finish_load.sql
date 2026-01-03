UPDATE load_history 
SET 
    status = %s,
    rooms_inserted = %s,
    rooms_updated = %s,
    rooms_deleted = %s,
    students_inserted = %s,
    students_updated = %s,
    students_deleted = %s,
    error_message = %s
WHERE load_id = %s