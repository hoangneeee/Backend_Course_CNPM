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

