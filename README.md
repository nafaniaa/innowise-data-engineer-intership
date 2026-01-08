# Students & Rooms Analyzer v1

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

# Students & Rooms Analyzer v2
ETL process for loading rooms and students data from JSON files into MySQL with incremental loading, full change history, and analytics.

## Main Features

- **Incremental loading** (INSERT/UPDATE/DELETE) — repeated runs update only changed records instead of truncating tables
- **Full change history**:
  - `load_history` — details of each load (timestamp, files, statistics)
  - `rooms_history` and `students_history` — every single change (INSERT/UPDATE/DELETE)
- **4 analytical queries**
- **Export results** to JSON (default) or XML
- **Logging** of all operations
- **Docker Compose** deployment with isolated MySQL database

## Project Structure
.

├── main.py                     # Entry point

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── .env                        # Create manually (see below)

├── src_data/

│   ├── rooms.json

│   └── students.json

├── sql_queries/

│   ├── ddl/                    # Table creation & history tables

│   ├── dml/                    # Loading operations

│   └── history/                # History-related queries

├── app/
│   ├── db/                     # Connection & SQLExecutor

│   ├── services/               # LoadService & AnalyticsService

│   └── exporters/              # JSON & XML exporters

└── results/                    # Created automatically — export results


## How to Run

### Recommended: Docker Compose

1. Make sure Docker and Docker Compose are installed.
2. Create `.env` file in the root with the following content:
- MYSQL_ROOT_PASSWORD=RootPass123!
- MYSQL_DATABASE=students_db
- MYSQL_USER=app_user
- MYSQL_PASSWORD=AppPass123!
- DB_HOST=db
- DB_PORT=3306
- DB_NAME=students_db
- DB_USER=app_user
- DB_PASSWORD=AppPass123!

3. Start the project:


docker-compose up --build
- The first run creates tables, loads data, performs analytics, and exports JSON results.
- Subsequent runs perform incremental updates only.
- To run with XML export:
Bashdocker-compose run --rm app python main.py --format xml
- Results will appear in the results/ folder.

- Quick Run with Docker Image (No Build)
  
docker run --rm \
  -v $(pwd)/results:/app/results \
  nafaniaaa/first-python-task:latest \
  --format json

docker run --rm \
  -v $(pwd)/results:/app/results \
  nafaniaaa/first-python-task:latest \
  --format xml


python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

