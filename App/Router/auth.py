from fastapi import APIRouter, status

from App.Schemas import admin as schemas_admin
from App.Objects import admin as objects_user
from App.DB import database as db
from App.Common import common
from App.Common.response import ResponseData
from App.Common import res_message


router = APIRouter()
APIVER = '1.0.0'

@router.post('/login', summary='Handle Login')
async def handle_login(user: schemas_admin.Login):
    print("/auth/login param=%s" % user)
    query = "select * from member where username='%s'" % user.username
    member_row = await db.database.database.fetch_one(query=query)

    if member_row is None:
        return ResponseData(status_code=status.HTTP_400_BAD_REQUEST, status_message=res_message.MEMBER_FAIL)

    username = member_row.get('username')

    if username is None:
        return ResponseData(status_code=status.HTTP_202_ACCEPTED, status_message=res_message.LOGIN_FAIL)
    else:
        member_id = member_row.get('id')
        member_group = member_row.get('member_group')
        hashed_password = member_row.get('password')
        plain_password = user.password
        if common.Hash.verify(hashed_password, plain_password, username):
            query = "select * from access_token where member_id=%s" % member_id
            select_row = await db.database.database.fetch_one(query=query)
            access_token = objects_user.AccessToken()

            if select_row.get('member_id') is None:
                # Create Access token
                access_token.access_token = common.create_access_token()
                await common.add_access_token(access_token.access_token, member_id, member_group)
                return ResponseData(status_code=status.HTTP_200_OK, data=access_token)
            else:
                # Update Access token
                access_token.access_token = common.create_access_token()
                await common.update_access_token(access_token.access_token, member_id)
                return ResponseData(status_code=status.HTTP_200_OK, data=access_token)
        else:
            return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.LOGIN_FAIL)

