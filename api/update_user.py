from datetime import date
from sqlite3 import Date
from xmlrpc.client import boolean
from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import update_user
from pydantic import BaseModel


class UpdateUser(BaseModel):
    id: int
    name: str
    gender: bool
    birthday: date
    phone: str
@app.put('/update-user')
def register(newuser: UpdateUser):
    result = update_user(newuser.id, newuser.name, newuser.gender, newuser.birthday, newuser.phone)
    
    if result is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return { "data": { 
                "user": result
                }
            }
