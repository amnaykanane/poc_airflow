
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.utils.task_group import TaskGroup

from datetime import datetime
import pandas as pd 
import numpy as np 

root = "/home/airflow/airflow/" # à modifier

csvs_paths = os.listdir(root + "data/")

default_args = {
    'start_date': datetime(2020, 1, 1)
}

# Python functions
def _sum_1(ti):
    print("summing with coeff 1")
    result = 0
    for path in csvs_paths:
        df = pd.read_csv(root + "data/" + path)
        result += df['0'].sum()
    print("sum_1 result: ", result)
    return ti.xcom_push(key='result',value=float(result))

def _sum_2(ti):
    print("summing with coeff 2")
    result = 0
    for path in csvs_paths:
        df = pd.read_csv(root + "data/" + path)
        result += df['0'].multiply(2).sum()
    print("sum_2 result: ", result)
    return ti.xcom_push(key='result',value=float(result))

def _divide(ti):
    print("dividing")
    results = ti.xcom_pull(key='result', task_ids=[
        "processing_tasks.summing_1",
        "processing_tasks.summing_2"
    ])
    output = results[1] / results[0]
    print(output)

# DAG object
with DAG('poc_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    downloading_data = BashOperator(
        task_id='downloading_data',
        bash_command='sleep 3',
        do_xcom_push=False
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        summing_1 = PythonOperator(
            task_id='summing_1',
            python_callable=_sum_1
        )

        summing_2 = PythonOperator(
            task_id='summing_2',
            python_callable=_sum_2
        )

    divide = PythonOperator(
        task_id='divide',
        python_callable=_divide
    )

# Dag Dependecies
downloading_data >> processing_tasks >> divide
