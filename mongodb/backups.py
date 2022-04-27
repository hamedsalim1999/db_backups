import docker
import logging
import subprocess
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
import os
import bson
load_dotenv()
logging.basicConfig(level=logging.INFO)
from pymongo import MongoClient



class MongoDB:
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
        conn = MongoClient(f"mongodb://{self.db_user}:{self.db_password }@{self.db_host}:{self.db_host_port}")
        return conn
    
    def dump(self,collections, db_name, path):
        conn = self.config_engine()
        db = conn[db_name]
        for coll in collections:
            with open(os.path.join(path, f'{coll}.bson'), 'wb+') as f:
                for doc in db[coll].find():
                    f.write(bson.BSON.encode(doc))

mongp = MongoDB("password","127.0.0.1","27017","hamed","mongo")
mongp.dump(["apples"],"fruits","/tmp/db")