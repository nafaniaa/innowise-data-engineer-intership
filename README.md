# Students & Rooms Analyzer

## Description
Python application that loads students and rooms data into MySQL database,
performs analytical SQL queries and exports results to JSON or XML.

## Requirements
- Python 3.10+
- MySQL
- No ORM (pure SQL)
- mysql-connector-python==9.5.0
- python-dateutil==2.9.0.post0
- python-dotenv==1.2.1
- six==1.17.0


## Setup
## Environment variables (.env)

- DB_HOST=localhost
- DB_PORT=3306
- DB_NAME=students_db
- DB_USER=root
- DB_PASSWORD=your_password

## Run
python main.py --students students.json --rooms rooms.json --format json

## Features

Many-to-one relationship (students → rooms)

All calculations performed at DB level

SQL optimization with indexes

OOP & SOLID principles

JSON / XML export

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
