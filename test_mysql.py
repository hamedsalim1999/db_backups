from pickle import NONE
from mysql.backups import MySql
from os import getenv
from dotenv import load_dotenv
import docker
import warnings

load_dotenv()
db_password = getenv('db_password')
db_host= getenv('db_host')
db_host_port = getenv('db_host_port')
db_user = getenv('db_user')
db_type= getenv('db_type')
try:
    container_name= getenv('container_name')
except:
    raise("you use none contiber database")

db = MySql(db_password, db_host, db_host_port, db_user, db_type,"/tmp/")

def db_connect():
    
    db_enggine = db.config_engine()
    try:
        with db_enggine.connect() as connection:
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

def test_get_mysql_database_list():
    db_list = db.get_mysql_database_list()
    assert "sys" in db_list
    
def test_mysql_backup_command():
    assert (db.mysql_backup_command("sys"),None)
        