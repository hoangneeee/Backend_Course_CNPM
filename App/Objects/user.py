from typing import List
from App.Objects import admin as object_admin


class MemberInfo(object):
    def __init__(self):
        self.id = 0
        self.create_time = ""
        self.update_time = ""
        self.username = ""
        self.age = 0
        self.gender = 0
        self.coin = 0
        self.gmail = ""
        self.phone = ""
        self.member_group = 0


class HistoryInfo(object):
    def __init__(self):
        self.id = 0
        self.member_id = 0
        self.course_id = object_admin.CourseInfo.__dict__
