import docker
import logging
import subprocess
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine 


load_dotenv()
logging.basicConfig(level=logging.INFO)

class MySql:
    def __init__(self,db_password:str, db_host:str, db_host_port:str, db_user:str, db_type:str,continer:bool=False,container_name:str=None) -> None:
        self.now = datetime.now().strftime("%m-%d-%Y") 
        self.db_password = db_password
        self.db_host = db_host
        self.db_host_port = db_host_port
        self.db_user = db_user
        self.db_type= db_type      
        self.continer = continer
        if self.continer :
            self.container_name = container_name  

    def config_engine(self):
        engine = create_engine(f"{self.db_type}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_host_port}")
        return engine
    
    def config_continer(self):
        client = docker.from_env()
        container = client.containers.get(self.container_name)
        return container  

    def get_mysql_database_list(self):
        
        if self.continer :
            container = self.config_continer()
            list_of_databases = logging.info(container.exec_run(f"mysql -h {self.db_host} --port={self.db_host_prot} -p{self.db_password} -e 'show databases;'").output.decode("utf-8").split("\n") )
        else:
            engine = self.config_engine()
            list_of_databases = [i[0] for i in engine.execute('SHOW DATABASES;').fetchall()]
        return list_of_databases

    def mysql_backup_command(self,database_name:str):
        if self.continer :
            container = self.config_continer()
            logging.info(container.exec_run(f"bash -c 'mysqldump -h {self.db_host} --port={self.db_host_prot} -p{self.db_password} {database_name}> /tmp/{self.now}-{database_name}.sql'"))
        else:
            subprocess.Popen(f"mysqldump -p{self.db_password} -u root  -h {self.db_host} {database_name}> /tmp/db/{self.now}-{database_name}.sql", shell=True)
    
    def back_up(self):
        try:
            databases = self.get_mysql_database_list()
        except:
            logging.error("Can't find databases list ")
        
        logging.info(list(map(self.mysql_backup_command,databases)))
