import docker
import logging
import subprocess
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
import re
from base.base import Main 
load_dotenv()
logging.basicConfig(level=logging.INFO)



class MongoDB(Main):
    def __init__(self,db_password:str, db_host:str, db_host_port:str, db_user:str, db_type:str,address:str,continer:bool=False,container_name:str=None) -> None:
        self.now = datetime.now().strftime("%m-%d-%Y") 
        self.db_password = db_password
        self.db_host = db_host
        self.db_host_port = db_host_port
        self.db_user = db_user
        self.db_type= db_type      
        self.address=re.sub(r"\/$","",address)
        self.continer = continer
        if self.continer :
            self.container_name = container_name  

    def config_continer(self):
        client = docker.from_env()
        container = client.containers.get(self.container_name)
        return container  
    
    def dump(self):
        if self.continer :
            container = self.config_continer()
            logging.info(container.exec_run(f"bash -c 'mongodump --host={self.db_host} --port={self.db_host_port} --username {self.db_user} --password {self.db_password} --out={self.address}/{self.now}'"))
        else:
            logging.info(subprocess.Popen(f"mongodump --host={self.db_host} --port={self.db_host_port} --username {self.db_user} --password {self.db_password} --out={self.address}/{self.now} --quiet", shell=True))

