import os
import datetime

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator

from mongodb import upload_to_mongo
from visualization \
    import \
        types_of_job_postings, \
        ds_job_postings_in_ffang, \
        proportion_of_relevant_postings, \
        average_salary
from models import random_forest, simple_linear_regression
from spark import save_spark_dataframe

with DAG(
    dag_id="example",
    start_date=datetime.datetime(2024, 2, 1),
    catchup=False,
    schedule=None,
    tags=["example"],
    params={
        'gcs_bucket_name' : 'msds697-jobs',
        'gcs_input_dir_path' : 'jobs',
        'output_dir_path' : '/tmp',
        'mongodb_host' : 'localhost',
        'mongodb_port' : '27017',
        'mongodb_database' : 'msds697',
        'mongodb_collection' : 'jobs'
    }
) as dag:
    gcs_input_file_path = os.path.join("{{ params.gcs_input_dir_path }}", 'jobs.json')
    output_file_path = os.path.join("{{ params.output_dir_path }}", 'jobs.json')
    parquet_path = os.path.join("{{ params.output_dir_path }}", 'parquets')

    gcs_download_task = GCSToLocalFilesystemOperator(
        task_id="download_file_from_gcs",
        bucket="{{ params.gcs_bucket_name }}",
        object_name=gcs_input_file_path,
        filename=output_file_path
    )

    mongodb_import_task = PythonOperator(
        task_id='upload_mongodb',
        python_callable=upload_to_mongo,
        op_kwargs={
            'host' : "{{ params.mongodb_host }}",
            'port' : "{{ params.mongodb_port }}",
            'database_name' : "{{ params.mongodb_database }}",
            'collection_name' : "{{ params.mongodb_collection }}",
            'input_file_path' : output_file_path
        }
    )

    visualization_tasks = [
        PythonOperator(
            task_id='types_of_job_postings',
            python_callable=types_of_job_postings,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'output_path' : "{{ params.output_dir_path }}"
            }
        ),
        PythonOperator(
            task_id='ds_job_postings_in_ffang',
            python_callable=ds_job_postings_in_ffang,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'output_path' : "{{ params.output_dir_path }}"
            }
        ),
        PythonOperator(
            task_id='proportion_of_relevant_postings',
            python_callable=proportion_of_relevant_postings,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'output_path' : "{{ params.output_dir_path }}"
            }
        ),
        PythonOperator(
            task_id='average_salary',
            python_callable=average_salary,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'input_path' : parquet_path,
                'output_path' : "{{ params.output_dir_path }}"
            }
        )
    ]

    spark_dataframe_task = PythonOperator(
        task_id='spark_dataframe_save',
        python_callable=save_spark_dataframe,
        op_kwargs={
            'host' : "{{ params.mongodb_host }}",
            'port' : "{{ params.mongodb_port }}",
            'database_name' : "{{ params.mongodb_database }}",
            'collection_name' : "{{ params.mongodb_collection }}",
            'output_path' : parquet_path
        }
    )

    modeling_task = [
        PythonOperator(
            task_id='random_forest',
            python_callable=random_forest,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'input_path' : parquet_path,
                'output_path' : "{{ params.output_dir_path }}"
            }
        ),
        PythonOperator(
            task_id='simple_linear_regression',
            python_callable=simple_linear_regression,
            op_kwargs={
                'host' : "{{ params.mongodb_host }}",
                'port' : "{{ params.mongodb_port }}",
                'database_name' : "{{ params.mongodb_database }}",
                'collection_name' : "{{ params.mongodb_collection }}",
                'input_path' : parquet_path,
                'output_path' : "{{ params.output_dir_path }}"
            }
        )
    ]

    gcs_download_task >> mongodb_import_task >> spark_dataframe_task
    spark_dataframe_task >> visualization_tasks[-1]
    spark_dataframe_task >> modeling_task
    mongodb_import_task.set_downstream(visualization_tasks)