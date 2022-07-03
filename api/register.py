from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import add_user, get_user_by_id
from services.account import add_account
from pydantic import BaseModel
from fastapi import FastAPI, Body, Depends,Form
from auth.auth_bearer import JWTBearer

class NewUser(BaseModel):
    name: str
    driver_license: str
    username: str
    password: str
    
# class User(BaseModel):
#     name: str
#     driver_license: str
@app.post('/register')
# def login (username: str, password: str):  name: str, driver_license: str
def register(token: str = Depends(JWTBearer()), newuser: NewUser = Body(...)):
    userid = decodeJWT(token)['user_id']
    user = get_user_by_id(userid) 
    if user.role.name.lower() != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")

    result_user = add_user(newuser.name, newuser.driver_license,newuser.username, newuser.password)
    if result_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = signJWT(user.id)

    return { "data": { 
                "access_token" :token,
                "user": result_user
                }
            }
