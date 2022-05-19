from typing import List
from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    age: int
    gender: int = 0
    gmail: str = ""
    phone: str
    member_group: int


class AddCart(BaseModel):
    member_id: int
    course_id: int
    total_price: float


class GetHistory(BaseModel):
    member_id: int

