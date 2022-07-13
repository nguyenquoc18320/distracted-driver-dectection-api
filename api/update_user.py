from datetime import date 
from sqlite3 import Date
from urllib import request
# from xmlrpc.client import boolean
from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import update_user
from pydantic import BaseModel
from fastapi import FastAPI, Body, Depends,Form
from auth.auth_bearer import JWTBearer

class UpdateUser(BaseModel):
    id: int
    name: str
    gender: bool
    birthday: date
    phone: str
@app.put('/update-user')
# def register(token: str = Depends(JWTBearer()), newuser: UpdateUser = Body(...)):
def update_User( newuser: UpdateUser = Body(...)):
    # userid = decodeJWT(token)['user_id']
    # user = get_user_by_id(userid) 
    # if user.role.name.lower() != 'admin':
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    result = update_user(newuser.id, newuser.name, newuser.gender, newuser.birthday, newuser.phone)
    alert = "Update Fail"
    if result is None:
        raise HTTPException(status_code=405, detail="Error")
    else:
        alert = 'Update Successfull'
    return { "data": { 
                "alert": alert,
                "user": result
                }
            }
