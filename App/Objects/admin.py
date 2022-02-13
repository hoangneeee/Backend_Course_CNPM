from typing import List
from App.Objects import user as object_user


class AccessToken(object):
    def __init__(self):
        self.access_token = ""
        self.member_info = object_user.MemberInfo.__dict__


class LessonInfo(object):
    def __init__(self):
        self.id = ""
        self.create_time = ""
        self.update_time = ""
        self.lesson_name = ""
        self.lesson_time = ""
        self.status = 0


class CourseInfo(object):
    def __init__(self):
        self.id = ""
        self.create_time = ""
        self.update_time = ""
        self.title = ""
        self.video = ""
        self.image = ""
        self.description = ""
        self.author_id = object_user.MemberInfo.__dict__
        self.price = ""
        self.status = ""
        self.lesson = LessonInfo.__dict__
