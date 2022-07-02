from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import add_user
from services.account import add_account
from pydantic import BaseModel
import datetime

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
def register(newuser: NewUser):
    # name = 'new'
    # driver_license = 'asdsasc3'
    result = add_user(newuser.name, newuser.driver_license,newuser.username, newuser.password)
    # result2 = add_account(newuser.username, newuser.password, result)
    # user_new = User(user.name, True, datetime.datetime(2022, 1,1), '0354316135', user.driver_license,"1" )
    # result = add_user()
    if result is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = signJWT(result.id)

    return { "data": { 
                "access_token" :token,
                "user": result
                }
            }
