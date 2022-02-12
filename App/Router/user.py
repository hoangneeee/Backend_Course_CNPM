from typing import Optional, List
from fastapi import APIRouter, status, Header

from App.Schemas import admin as schemas_admin
from App.Schemas import user as schemas_user
from App.Objects import user as objects_user
from App.Objects import admin as objects_admin
from App.DB import database as db
from App.Common import common
from App.Common.response import ResponseData
from App.Common import res_message

router = APIRouter()
APIVER = '1.0.0'


@router.post('/register', summary='Handle Register')
async def handle_register(user: schemas_user.UserRegister):
    print("/user/register param=%s" % user.__dict__)
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


@router.post('/course_get', summary='Get Course Information')
async def get_all_course(course: schemas_admin.GetCourse, access_token: Optional[str] = Header(None, convert_underscores=True)):
    print("/user/course param=%s" % course.__dict__)
    member_group = await common.verify_token(access_token)
    if member_group != 0 and member_group != 1 and member_group != 2:
        return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)

    response_info: List[objects_admin.CourseInfo] = []
    # Get All Course
    if course.id == 0:
        query = "select * from course"
        course_rows = await db.database.database.fetch_all(query=query)

        if course_rows is None:
            return ResponseData(status_code=status.HTTP_200_OK, data={'courses': response_info})

        # Response Course
        for course_row in course_rows:
            course_info = objects_admin.CourseInfo()
            for item in course_row:
                for key in vars(course_info).keys():
                    if key == item:
                        course_info.__dict__[key] = course_row.get(item)
                        break

            lesson_ids = course_row.get('lesson')
            lesson = []
            for lesson_id in lesson_ids:
                query = "select * from lesson where id=%s" % lesson_id
                lesson_rows = await db.database.database.fetch_one(query=query)
                lesson_info = objects_admin.LessonInfo()
                for item in lesson_rows:
                    for key in vars(lesson_info).keys():
                        if key == item:
                            lesson_info.__dict__[key] = lesson_rows.get(item)
                            break
                lesson.append(lesson_info.__dict__)
                course_info.lesson = lesson

            response_info.append(course_info)

        return ResponseData(status_code=status.HTTP_200_OK, data={'courses': response_info})
    else:
        # Get Course with ID
        query = "select * from course where id=%s" % course.id
        course_row = await db.database.database.fetch_one(query=query)

        if course_row is None:
            return ResponseData(status_code=status.HTTP_200_OK, data={'courses': response_info})

        # Response Course
        course_info = objects_admin.CourseInfo()
        for item in course_row:
            for key in vars(course_info).keys():
                if key == item:
                    course_info.__dict__[key] = course_row.get(item)
                    break

        lesson_ids = course_row.get('lesson')
        lesson = []
        for lesson_id in lesson_ids:
            query = "select * from lesson where id=%s" % lesson_id
            lesson_rows = await db.database.database.fetch_one(query=query)
            lesson_info = objects_admin.LessonInfo()
            for item in lesson_rows:
                for key in vars(lesson_info).keys():
                    if key == item:
                        lesson_info.__dict__[key] = lesson_rows.get(item)
                        break
            lesson.append(lesson_info.__dict__)
            course_info.lesson = lesson

        response_info.append(course_info)

        return ResponseData(status_code=status.HTTP_200_OK, data={'courses': response_info})

