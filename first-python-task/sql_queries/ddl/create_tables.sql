CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATETIME NOT NULL,
    sex CHAR(1) NOT NULL,
    room_id INT NOT NULL,
    CONSTRAINT fk_students_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
