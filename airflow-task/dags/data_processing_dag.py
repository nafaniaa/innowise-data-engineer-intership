from airflow.decorators import dag, task_group
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow import Dataset
import csv

from datetime import datetime
import os
import pandas as pd


processed_dataset = Dataset("processed_comments") #logical object

INPUT_FILE = "/data/input.csv"
OUTPUT_FILE = "/data/processed.csv"


"""
Function for checking empty file
"""
def check_if_file_empty():
    if os.path.getsize(INPUT_FILE) == 0:
        return "log_empty_file"
    else:
        return "processing_group.replace_nulls"


"""
Replace all "null" values with "-";
"""

def replace_nulls():
    cleaned_rows = []
    
    with open(INPUT_FILE, 'r', encoding='latin1', errors='replace') as f:
        reader = csv.reader(f, delimiter=',')
        try:
            header = next(reader)
            num_columns = len(header)
        except StopIteration:
            return

        for row in reader:
            if len(row) == num_columns:
                cleaned_rows.append(row)

    df = pd.DataFrame(cleaned_rows, columns=header)
    
    df = df.fillna("-")
    df = df.replace(["null", "Null", "NULL"], "-")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')


"""
Sort data by created_date
"""

def sort_by_date():
    df = pd.read_csv(OUTPUT_FILE)
    df.sort_values(by = "at", inplace = True)
    df.to_csv(OUTPUT_FILE, index = False)

"""
Remove all unnecessary characters from the content column 
(e.g. smiley faces, etc.), 
leaving only text and punctuation marks.
"""
def clean_content():
    df = pd.read_csv(OUTPUT_FILE)
    df["content"] = df["content"].str.replace(
        r"[^a-zA-Z0-9\s.,!?]", "", regex=True
    )
    df.to_csv(OUTPUT_FILE, index=False)


@dag(
    dag_id = "data_processing_dag",
    start_date = datetime(2024, 1, 1),
    schedule = None,
    catchup = False,
    tags=["processing"],
)
def data_processing_dag():
    #Sensor
    wait_for_file = FileSensor(
        task_id = "wait_for_file",
        filepath = INPUT_FILE,
        fs_conn_id="fs_default",
        poke_interval=30,
        timeout=60 * 5,
        mode="reschedule",
    )

    #Branch
    branch = BranchPythonOperator(
        task_id = "check_file",
        python_callable = check_if_file_empty
    )

    #If file empty, BashOperator
    log_empty = BashOperator(
        task_id = "log_empty_file",
        bash_command = 'echo "Empty file"'
    )

    #TaskGroup
    @task_group(group_id = "processing_group")
    def processing_group():
        task_replace = PythonOperator(
            task_id = "replace_nulls",
            python_callable = replace_nulls
        )

        task_sort = PythonOperator(
            task_id = "sort_by_date",
            python_callable = sort_by_date
        )

        task_clean = PythonOperator(
            task_id="clean_content",
            python_callable=clean_content,
            outlets=[processed_dataset],
        )

        task_replace >> task_sort >> task_clean

  
    processing_tasks = processing_group()


    wait_for_file >> branch
    branch >> [log_empty, processing_tasks]


data_processing_dag = data_processing_dag()