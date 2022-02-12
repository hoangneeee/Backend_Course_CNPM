from typing import List


class AccessToken(object):
    def __init__(self):
        self.access_token = ""


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
        self.author_id = ""
        self.price = ""
        self.status = ""
        self.lesson = LessonInfo.__dict__
