import re
from mongodb.backups import MongoDB
from os import getenv
from dotenv import load_dotenv
import docker
from pymongo import MongoClient

load_dotenv()
db_password = getenv('db_password')
db_host= getenv('db_host')
db_host_port = int(getenv('db_host_port'))
db_user = getenv('db_user')
db_type= getenv('db_type')


try:
    container_name= getenv('container_name')
except:
    raise("you use none contiber database")

db = MongoDB(db_password, db_host, db_host_port, db_user, db_type,"/tmp/")

def db_connect():
    client = MongoClient(db.db_host,
                    username=db.db_user,
                    password=db.db_password,
                    connectTimeoutMS=3000
                    )
    try:
        client.server_info()
        return True
    except:
        return False

def db_continer():
    client = docker.from_env()
    try:
        client.containers.get(container_name)
        return True
    except:
        return False
    
def test_dabasa_connect():
    assert db_connect() == True
if container_name:
    def test_config_continer():
        assert db_continer() == True


        

