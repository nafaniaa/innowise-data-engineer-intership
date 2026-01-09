SET @idx_exists := (
    SELECT COUNT(1)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'students'
      AND index_name = 'idx_students_room_id'
);

SET @sql := IF(
    @idx_exists = 0,
    'CREATE INDEX idx_students_room_id ON students(room_id)',
    'SELECT ''Index idx_students_room_id already exists'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


SET @idx_exists := (
    SELECT COUNT(1)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'students'
      AND index_name = 'idx_students_sex'
);

SET @sql := IF(
    @idx_exists = 0,
    'CREATE INDEX idx_students_sex ON students(sex)',
    'SELECT ''Index idx_students_sex already exists'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


SET @idx_exists := (
    SELECT COUNT(1)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'students'
      AND index_name = 'idx_students_birthday'
);

SET @sql := IF(
    @idx_exists = 0,
    'CREATE INDEX idx_students_birthday ON students(birthday)',
    'SELECT ''Index idx_students_birthday already exists'''
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;