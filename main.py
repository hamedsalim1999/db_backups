import docker
import logging
from os import getenv
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
now = datetime.now().strftime("%m-%d-%Y") 


db_password = getenv('db_password')
db_host= getenv('db_host')
db_host_port = getenv('db_host_port')


logging.basicConfig(level=logging.INFO)
client = docker.from_env()
container = client.containers.get('some-mysql')



def get_mysql_database_list(password,host=db_host,prot=db_host_port):
    list_of_databases = container.exec_run(f"mysql -h {host} --port={prot} -p{password} -e 'show databases;'").output.decode("utf-8").split("\n") 
    return list_of_databases


def mysql_backup(password,database_name,host=db_host,prot=db_host_port):
    logging.info(container.exec_run(f"bash -c 'mysqldump -h {host} --port={prot} -p{password} {database_name}> /tmp/{now}-{database_name}.sql'"))
    return f"{database_name} is Done"


try:
    databases = get_mysql_database_list(db_password)
except:
    pass


if "[Warning]" in databases[0]:
    databases.pop(0)
    try:
        databases = list(filter(None, databases))
    except:
        pass


logging.info(list(map(mysql_backup,db_password,databases)))

