import os
import databases
import sqlalchemy
from dotenv import load_dotenv
from App.Common import common


load_dotenv()


class database():

    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
        DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

    # databases
    database = databases.Database(DATABASE_URL, min_size=5, max_size=20)

    ECHO_LOG = False

    engine = sqlalchemy.create_engine(DATABASE_URL, echo=ECHO_LOG)

    metadata = sqlalchemy.MetaData()


def get_insert_query(tableName, rows, value):
    return 'insert into %s(%s) values(%s)' % (tableName, rows, value)


def get_delete_query(tableName, where, value):
    return "delete from %s where %s=%s" % (tableName, where, value)

