import string
import base64
import secrets
from datetime import datetime, timezone, timedelta, date


from App.DB import database as db


def insert_string(string, index, plus_string):
    return string[:index] + plus_string + string[index:]



def get_now_time():
    ''' Get Time VN Now'''

    VN = timezone(timedelta(hours=+7), 'VN')
    now = datetime.now(VN)
    nowStr = now.strftime('%Y%m%d%H%M%S')

    return nowStr


def get_date(month_flg: bool = False):
    ''' Get Date VN Now '''

    VN = timezone(timedelta(hours=+7), 'VN')
    now = datetime.now(VN)
    date = now.strftime('%Y%m%d')
    if month_flg:
        date = now.strftime('%Y%m')

    return date


def create_access_token():
    ''' Create Access Token '''

    access_token = ''.join(
        [secrets.choice(string.ascii_letters + string.digits) for i in range(130)])

    return access_token


async def verify_token(token:str):
    ''' Verify Access Token '''

    query = "select * from access_token where access_token='%s'" %token
    select_row = await db.database.database.fetch_one(query=query)
    if select_row is None:
        return -1

    access_token = select_row.get('access_token')

    if token == access_token:
        return select_row.get('member_group')
    else:
        return -1


async def add_access_token(access_token, member_id, member_group):
    ''' Add Access Token '''

    row = "access_token, member_id, member_group"
    values = "'%s', %s, '%s' " % (
        access_token,
        member_id,
        member_group
    )
    query = db.get_insert_query('access_token', row, values)
    await db.database.database.execute(query=query)


async def update_access_token(access_token, member_id):
    ''' Update Access Token '''

    row = "access_token='%s'" % access_token
    where = "member_id=%s" % member_id
    query = "update access_token set %s where %s" % (row, where)
    await db.database.database.execute(query=query)


class Hash():
    '''Hash Password Section'''

    def hashing(password: str, username: str):
        password_encrypt = password + ' ' + username
        password_bytes = base64.b64encode(password_encrypt.encode('ascii'))
        password_hash = password_bytes.decode("ascii")

        return password_hash

    def verify(hashed_password, plain_password, username):
        plain_password = plain_password + ' ' + username
        password_bytes = hashed_password.encode("ascii")
        password_hash = base64.b64decode(password_bytes).decode("ascii")

        return password_hash == plain_password

    def decrypt(hashed_password):
        password_bytes = hashed_password.encode("ascii")
        password_hash = base64.b64decode(password_bytes).decode("ascii").split()

        return password_hash[0]

