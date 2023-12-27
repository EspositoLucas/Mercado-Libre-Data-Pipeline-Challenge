from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator 
from datetime import datetime
from operators.PostgresFileOperator import PostgresFileOperator
from airflow.operators.bash import BashOperator
import datetime

DATE = str(datetime.date.today()).replace('-','')

with DAG(
    dag_id="postgres",
    start_date= datetime(2023,12,27),
    #schedule_interval='@ @ * * *'
)as dag:
    task_1 = PostgresOperator(
    task_id="create_table",
    postgres_conn_id = "postgres_localhost", 
    sql= """
        create table if not exists mercado_libre_data (
        id varchar(100), 
        site_id varchar(100), 
        title varchar(100),
        price varchar(100),
        sold_quantity varchar(100),
        thumbnail varchar(100),
        created_date varchar(100),
        primary key(id, created_date)  
        
    )
    """
),
    task_2 = BashOperator(
    task_id = "consulting_API",
    bash_command = "python /opt/airflow/plugins/tmp/api_fetch.py"

),   
    
    task_3 = PostgresFileOperator(
    task_id = "insert_data",
    operation="write",
    config={"table_name":"mercado_libre_data"}
),
    task_4 = PostgresFileOperator(
    task_id = "reading_data",
    operation="read",
    config={"query":"select * from mercado_libre_data mld where mld.sold_quantity  != 'null' and cast(mld.price as decimal) * cast(mld.sold_quantity as int) > 7000000"}  
)
