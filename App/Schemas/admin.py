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


class GetCourse(BaseModel):
    id: int
