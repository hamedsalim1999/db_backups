from distutils.log import error
import docker
import logging
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
import subprocess
from sqlalchemy import create_engine 


load_dotenv()
now = datetime.now().strftime("%m-%d-%Y") 


db_password = getenv('db_password')
db_host= getenv('db_host')
db_host_port = getenv('db_host_port')
db_user = getenv('db_user')
db_type= getenv('db_type')


engine = create_engine(f"{db_type}://{db_user}:{db_password}@{db_host}:{db_host_port}")

logging.basicConfig(level=logging.INFO)
client = docker.from_env()
container = client.containers.get('some-mysql')



def get_mysql_database_list(password,host=db_host,prot=db_host_port,continer=False):
    if continer :
        list_of_databases = logging.info(container.exec_run(f"mysql -h {host} --port={prot} -p{password} -e 'show databases;'").output.decode("utf-8").split("\n") )
    else:
        list_of_databases = [i[0] for i in engine.execute('SHOW DATABASES;').fetchall()]
    return list_of_databases


def mysql_backup(database_name,password=db_password,host=db_host,prot=db_host_port,continer=False):
    if continer :
        logging.info(container.exec_run(f"bash -c 'mysqldump -h {host} --port={prot} -p{password} {database_name}> /tmp/{now}-{database_name}.sql'"))
    else:
        subprocess.Popen(f"mysqldump -p{password} -u root  -h {host} {database_name}> /tmp/db/{now}-{database_name}.sql", shell=True)
    return f"{database_name} is Done"


# try:
#     databases = get_mysql_database_list(db_password)
# except:
#     print("ERROR")

databases = get_mysql_database_list(db_password)

if "[Warning]" in databases[0]:
    databases.pop(0)
    try:
        databases = list(filter(None, databases))
    except:
        pass


logging.info(list(map(mysql_backup,databases)))



