from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook 
import json
import smtplib
import ssl
from email.message import EmailMessage
from airflow.models import Variable
import datetime


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
        self.postgres_hook.bulk_load(self.config.get('table_name'),'plugins/tmp/file.tsv')
        

    def readFromDb(self):
    # read from db with a SQL query
        conn = self.postgres_hook.get_conn() 
        cursor = conn.cursor()
        cursor.execute(self.config.get("query"))
        
        data = [doc for doc in cursor]
        print (data)      
        
        

        if data: # if there are query results
        
        #send mail
            email_from ="user@gmail.com" 
            passw = Variable.get("password") 
            email_to= "user@gmail.com"
            title = "ALERT ! Items with too much sales" 
            body = """
            We have detected new items with too much sales: {}
            """.format(data)
            
            email = EmailMessage() 
            email['From'] = email_from
            email['To'] = email_to 
            email['Subject'] = title 
            email.set_content(body)
            

            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_from, passw)
                smtp.sendmail(email_from, email_to, email.as_string()) 
