CREATE TABLE IF NOT EXISTS load_history (
    load_id INT AUTO_INCREMENT PRIMARY KEY,
    load_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    rooms_file VARCHAR(255),
    students_file VARCHAR(255),
    rooms_inserted INT DEFAULT 0,
    rooms_updated INT DEFAULT 0,
    rooms_deleted INT DEFAULT 0,
    students_inserted INT DEFAULT 0,
    students_updated INT DEFAULT 0,
    students_deleted INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'SUCCESS',
    error_message TEXT NULL
);

CREATE TABLE IF NOT EXISTS rooms_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    load_id INT NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    room_id INT NOT NULL,
    room_name VARCHAR(255),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (load_id) REFERENCES load_history(load_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS students_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    load_id INT NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    student_id INT NOT NULL,
    student_name VARCHAR(255),
    birthday DATETIME,
    sex CHAR(1),
    room_id INT,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (load_id) REFERENCES load_history(load_id) ON DELETE CASCADE
);