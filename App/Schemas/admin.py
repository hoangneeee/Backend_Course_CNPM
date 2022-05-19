from typing import List
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class LessonInfo(BaseModel):
    lesson_name: str
    status: int = 1
    lesson_time: str


class CreateCourse(BaseModel):
    title: str
    video: str
    image: str
    description: str
    author_id: int
    price: float
    status: int = 1
    lessons: List[LessonInfo]


class UpdateCourse(BaseModel):
    id: int
    title: str
    video: str
    image: str
    description: str
    author_id: int
    price: float
    status: int = 1
    lessons: List[int]


class GetCourse(BaseModel):
    id: int


class RemoveCourse(BaseModel):
    course_id: int


class RemoveUser(BaseModel):
    user_id: int
