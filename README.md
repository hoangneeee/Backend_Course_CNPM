#**Backend Course CNPM**

_Author: Vo Hoang_

_Phone: 0349245719_

_Gmail: levuthanhtung11@gmail.com_

_Description: A small project about a course website written by myself_

**Command**

##Tạo môi trường phát triển
_Sửa file .env_

_Chạy câu lệnh sau để khởi tạo môi trường phát triển_

`docker-compose up -d`

_Install Package_

`pip install -r requirements.txt`

_Init Database_

`python init_db.py all`

_Run App_

`uvicorn main:app --reload`