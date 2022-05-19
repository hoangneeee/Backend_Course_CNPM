import databases
import sys
import asyncio
import os

from dotenv import load_dotenv
# from App.Common import common
# from App.DB.database import database as db


load_dotenv()

# Config DB
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

database = databases.Database(DATABASE_URL, min_size=5, max_size=20)


# Create Table
async def create_member():
    tableName = 'member'
    await database.connect()

    query = 'drop table if exists %s' % (tableName)
    await database.fetch_all(query)
    query = ''' create table %s(
                id                     serial primary key,
                create_time            char(14),
                update_time            char(14),
                username               text,
                password               text,
                age                    integer,
                gender                 integer,
                coin                   float,
                gmail                  text,
                phone                  text,
                member_group           integer
                )
            ''' % (tableName)
    await database.fetch_all(query)
    await database.disconnect()

    print(tableName + ' create complete')


async def create_course():
    tableName = 'course'
    await database.connect()

    query = 'drop table if exists %s' % (tableName)
    await database.fetch_all(query)
    query = ''' create table %s(
                id                      serial primary key,
                create_time             char(14),
                update_time             char(14),
                title                   text,
                video                   text,
                image                   text,
                description             text,
                author_id               integer,
                price                   float,
                status                  integer,
                lesson                  integer[]
                )
            ''' % (tableName)
    await database.fetch_all(query)
    await database.disconnect()

    print(tableName + ' create complete')


async def create_lesson():
    tableName = 'lesson'
    await database.connect()

    query = 'drop table if exists %s' % (tableName)
    await database.fetch_all(query)
    query = ''' create table %s(
                id                      serial primary key,
                create_time             char(14),
                update_time             char(14),
                lesson_name             text,
                status                  integer,
                lesson_time             text
                )
            ''' % (tableName)
    await database.fetch_all(query)
    await database.disconnect()

    print(tableName + ' create complete')


async def create_cart():
    tableName = 'cart'
    await database.connect()

    query = 'drop table if exists %s' % (tableName)
    await database.fetch_all(query)
    query = ''' create table %s(
                id                      serial primary key,
                create_time             char(14),
                update_time             char(14),
                member_id               integer,
                course_id               integer[],
                total_price             float,
                is_delete               boolean
                )
            ''' % (tableName)
    await database.fetch_all(query)
    await database.disconnect()

    print(tableName + ' create complete')


async def create_access_token():
    tableName = 'access_token'
    await database.connect()

    query = 'drop table if exists %s' % (tableName)
    await database.fetch_all(query)
    query = ''' create table %s(
                access_token            text,
                member_id               integer,
                member_group            integer 
                )
            ''' % (tableName)
    await database.fetch_all(query)
    await database.disconnect()

    print(tableName + ' create complete')


# async def create_user_admin(password, username):
#     cur_time = common.get_now_time()
#     passwd_hash = common.Hash.hashing(password, username)
#     rows = "create_time, update_time, username, password, age, gender, coin, gmail, phone, member_group"
#     values = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," % (
#         cur_time,
#         cur_time,
#         username,
#         passwd_hash,
#         0,
#         0,
#         0,
#         os.getenv('GMAIL'),
#         os.getenv('PHONE'),
#         0
#     )
#     query = db.database.get_insert_query("member", rows, values)
#     await db.database.database.execute(query=query)


# *******************************************************************
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    print(DATABASE_URL)
    args = sys.argv

    if len(args) < 2:
        print('Usage: init_db.py [sysInfo] [all]')
        '''
        s1 = 'spotId'
        s2 = camelTosnake( s1 )
        print( s1 +' > '+ s2 )
        s3 = snakeTocamel( s2 )
        print( s2 +' > '+ s3 )
        '''

    loop = asyncio.get_event_loop()

    for i in range(1, len(args)):
        cmd = args[i]
        if cmd == 'all':
            loop.run_until_complete(create_member())
            loop.run_until_complete(create_course())
            loop.run_until_complete(create_lesson())
            loop.run_until_complete(create_cart())
            loop.run_until_complete(create_access_token())
            # loop.run_until_complete(create_user_admin(os.getenv('PASSWORD'), os.getenv('USER_PASSWORD')))

