from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable 
import json
import smtplib
import ssl
from email.message import EmailMessage
import datetime
import os



DATE=str(datetime.date.today()).replace('-','')
class PostgresFileOperator (BaseOperator):
    @apply_defaults
    def __init__(self,operation, config={}, *args, **kwargs):
        super(PostgresFileOperator, self).__init__(*args, **kwargs)
        self.operation = operation
        self.config = config
        self.postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
        
        

    def execute(self, context):
        if self.operation == "write": 
            self.writeInDb()
        elif self.operation == "read":
            self.readFromDb()

    def writeInDb(self):
        # Use absolute path within container
        file_path = os.path.join('/opt/airflow', 'plugins/tmp/file.tsv')
        
        # Verify file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TSV file not found at {file_path}")
            
        self.postgres_hook.bulk_load(self.config.get('table_name'), file_path)

        

    def readFromDb(self):
        conn = self.postgres_hook.get_conn() 
        cursor = conn.cursor()
        cursor.execute(self.config.get("query"))
        
        data = [doc for doc in cursor]
        print("Query results:", data)      
        
        if data: # if there are query results
            try:
                email_from = "espositolucas2002@gmail.com" 
                # Get password from Airflow variable instead of env
                passw = Variable.get("EMAIL_PASSWORD")
                
                if not passw:
                    raise ValueError("EMAIL_PASSWORD not found in Airflow variables")
                    
                print(f"Attempting to send email with password length: {len(passw)}")
                
                email_to = "espositolucas2002@gmail.com"
                title = "ALERT ! Items with too much sales" 
                body = f"""
                We have detected new items with too much sales: {data}
                """
                
                email = EmailMessage() 
                email['From'] = email_from
                email['To'] = email_to 
                email['Subject'] = title 
                email.set_content(body)
                
                context = ssl.create_default_context()
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    print("Connecting to SMTP server...")
                    smtp.login(email_from, passw)
                    print("Login successful")
                    smtp.sendmail(email_from, email_to, email.as_string())
                    print("Email sent successfully")
                    
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                raise