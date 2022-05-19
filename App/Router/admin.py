from typing import Optional
from fastapi import APIRouter, status, Header

from App.Schemas import admin as schemas_admin
from App.Schemas import user as schemas_user
from App.Objects import admin as objects_user
from App.DB import database as db
from App.Common import common
from App.Common.response import ResponseData
from App.Common import res_message

router = APIRouter()
APIVER = '1.0.0'


@router.post('/create_course', summary='Create Course')
async def create_course(course: schemas_admin.CreateCourse, access_token: Optional[str] = Header(None, convert_underscores=True)):
    print("/admin/course param=%s" % course.__dict__)
    cur_time = common.get_now_time()
    member_group = await common.verify_token(access_token)
    if member_group != 0:
        return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)

    # Insert Lesson
    lessons = course.lessons
    lessons_id = []

    for lesson in lessons:
        row = "create_time, update_time, lesson_name, lesson_time, status"
        value = "'%s', '%s', '%s', '%s', '%s'" % (
            cur_time,
            cur_time,
            lesson.lesson_name,
            lesson.lesson_time,
            lesson.status
        )
        query = db.get_insert_query('lesson', row, value)
        await db.database.database.execute(query=query)
        query = "select * from lesson where lesson_name='%s' order by id desc" % lesson.lesson_name
        lesson_row = await db.database.database.fetch_one(query=query)
        lessons_id.append(lesson_row.get('id'))

    # Insert Course
    row = "create_time, update_time, title, video, image, description, author_id, price, status"
    value = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (
        cur_time,
        cur_time,
        course.title,
        course.video,
        course.image,
        course.description,
        course.author_id,
        course.price,
        course.status
    )
    query = db.get_insert_query('course', row, value)
    await db.database.database.execute(query=query)

    query = "select * from course where title='%s' and author_id=%s  order by id desc" % (course.title, course.author_id)
    course_row = await db.database.database.fetch_one(query=query)

    for lesson in lessons_id:
        row = "lesson=array_append(lesson, %s)" % (lesson)
        where = "id=%s" % (course_row.get('id'))
        query = "update course set %s where %s" % (row, where)
        await db.database.database.execute(query=query)

    return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.CREATE_COURSE_SUCCESS)


@router.post('/update_course', summary='Update Course')
async def create_course(course: schemas_admin.UpdateCourse, access_token: Optional[str] = Header(None, convert_underscores=True)):
    print("/admin/update_course param=%s" % course.__dict__)
    cur_time = common.get_now_time()
    member_group = await common.verify_token(access_token)
    if member_group != 0:
        return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)

    row = "title='%s', video='%s', image='%s', description='%s', price='%s', status='%s'" % (
        course.title,
        course.video,
        course.image,
        course.description,
        course.price,
        course.status
    )
    where = "id=%s" % course.id
    query = "update course set %s where %s" % (row, where)
    await db.database.database.execute(query=query)

    return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)


@router.post('/remove_course', summary='Remove Course')
async def handle_register(course: schemas_admin.RemoveCourse, access_token: Optional[str] = Header(None, convert_underscores=True)):
    print("/admin/remove_course param=%s" % course.__dict__)

    member_group = await common.verify_token(access_token)
    if member_group != 0:
        return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)

    query = "select * from course where id=%s" % course.course_id
    course_row = await db.database.database.fetch_one(query=query)

    # Remove Lesson
    lesson_ids = course_row.get('lesson')
    for lesson_id in lesson_ids:
        query = await db.get_delete_query('lesson', 'id', lesson_id)
        await db.database.database.execute(query=query)

    # Remove Course
    query = await db.get_delete_query('course', 'id', course.course_id)
    await db.database.database.execute(query=query)


@router.post('/remove_user', summary='Remove User')
async def remove_user(course: schemas_admin.RemoveUser, access_token: Optional[str] = Header(None, convert_underscores=True)):
    print("/admin/remove_user param=%s" % course.__dict__)

    member_group = await common.verify_token(access_token)
    if member_group != 0:
        return ResponseData(status_code=status.HTTP_200_OK, status_message=res_message.NOT_ALLOWED)

