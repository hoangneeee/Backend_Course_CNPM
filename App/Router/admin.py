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


@router.post('/course', summary='Create Course')
async def handle_register(course: schemas_admin.CreateCourse, access_token: Optional[str] = Header(None, convert_underscores=True)):
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
