import logging
from os import getenv
from dotenv import load_dotenv
from mysql.backups import MySql


load_dotenv()


db_password = getenv('db_password')
db_host= getenv('db_host')
db_host_port = getenv('db_host_port')
db_user = getenv('db_user')
db_type= getenv('db_type')




def main():
    db_connect = MySql(db_password, db_host, db_host_port, db_user, db_type)
    logging.info(db_connect.back_up())


if __name__ == "__main__":
    main()
else:
   print("File one executed when imported")