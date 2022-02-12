from fastapi import APIRouter, status

from App.Schemas import admin as schemas_admin
from App.Schemas import user as schemas_user
from App.Objects import user as objects_user
from App.DB import database as db
from App.Common import common
from App.Common.response import ResponseData
from App.Common import res_message

router = APIRouter()
APIVER = '1.0.0'


@router.post('/register', summary='Handle Register')
async def handle_register(user: schemas_user.UserRegister):
    print("/user/register param=%s" % user)
    cur_time = common.get_now_time()
    hash_password = common.Hash.hashing(user.password, user.username)

    # Validate Member Values
    query = "select * from member where username='%s'" % user.username
    member_row = await db.database.database.fetch_one(query=query)

    if member_row is not None:
        return ResponseData(status_code=status.HTTP_200_OK, status_message='Username đã tồn tại')
    if len(user.phone) < 10:
        return ResponseData(status_code=status.HTTP_200_OK, status_message='Số điện thoại không hợp lệ')
    if user.member_group == 0:
        return ResponseData(status_code=status.HTTP_200_OK, status_message='Không thể đăng ký quyền Admin')


    # Insert Member
    row = "create_time, update_time, username, password, age, gender, coin, gmail, phone, member_group"
    value = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (
        cur_time,
        cur_time,
        user.username,
        hash_password,
        user.age,
        user.gender,
        0,
        user.gmail,
        user.phone,
        user.member_group
    )
    query = db.get_insert_query('member', row, value)
    await db.database.database.execute(query=query)

    # Response Member info
    query = "select * from member where username='%s'" % user.username
    member_row = await db.database.database.fetch_one(query=query)
    member_info = objects_user.MemberInfo()
    for item in member_row:
        for key in vars(member_info).keys():
            if key == item:
                member_info.__dict__[key] = member_row.get(item)
                break
    return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.REGISTER_SUCCESS, data=member_info)
