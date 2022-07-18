from urllib import request
from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from fastapi import FastAPI, Body, Depends,Form
from auth.auth_bearer import JWTBearer
from services.account import get_account_by_user, passwordupdate
from pydantic import BaseModel

from services.user import get_user_by_id

class Update_Password(BaseModel):
    id: int
    newpassword: str
@app.put('/password_update')
def password_update(token: str = Depends(JWTBearer()),updatepass: Update_Password = Body(...)):
# def password_update(updatepass: Update_Password = Body(...)):
    alert = 'Fail'
    userid = decodeJWT(token)['user_id']
    user = get_user_by_id(userid) 
    if user.role.name.lower() != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")
    account_current = get_account_by_user(updatepass.id)
    if account_current is None:
        alert = 'Account does not exist!!!'
    else:
        if passwordupdate(account_current, updatepass.newpassword):
            user_request = get_user_by_id(updatepass.id)
            alert = 'Update Successfull'
    # token = signJWT(user.id)
    return { "data": { 
                "request" :alert,
                "user": user_request
                }
            } 
    
   
