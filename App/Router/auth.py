from fastapi import APIRouter
from databases import Database

router = APIRouter()
APIVER = '1.0.0'

@router.get('/login', summary='Handle Login')
async def handle_login():
    print('oke')
    return 'Oke'
