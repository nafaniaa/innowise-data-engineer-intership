from airflow.decorators import dag, task
from airflow.datasets import Dataset
from airflow.providers.mongo.hooks.mongo import MongoHook

from datetime import datetime
import pandas as pd



processed_dataset = Dataset("processed_comments") 

INPUT_FILE = "/data/processed.csv"


@dag(
    dag_id="load_to_mongo_dag",
    start_date=datetime(2024, 1, 1),
    schedule=[processed_dataset], 
    catchup=False,
    tags=["mongo", "load"],
)
def load_to_mongo_dag():

    @task
    def load_to_mongodb():
        df = pd.read_csv(INPUT_FILE)

        if "at" in df.columns:
            df["at"] = pd.to_datetime(df["at"])

        hook = MongoHook(conn_id="mongo_default")
        client = hook.get_conn()

        db = client["airflow_db"]
        collection = db["reviews"]

        collection.delete_many({})

        records = df.to_dict("records")
        if records:
            collection.insert_many(records)

    load_to_mongodb()


dag = load_to_mongo_dag()