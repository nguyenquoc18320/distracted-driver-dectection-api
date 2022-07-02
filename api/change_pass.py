from urllib import request
from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account

from services.account import get_account_by_user, passwordupdate
from pydantic import BaseModel

from services.user import get_user_by_id

class Update_Password(BaseModel):
    id: int
    oldpassword: str
    newpassword: str
@app.put('/password_update')
def password_update(updatepass: Update_Password):
    request = 'Fail'
    
    account_current = get_account_by_user(updatepass.id)
    if account_current is None:
        request = 'Account does not exist!!!'
    else:
        if passwordupdate(account_current, updatepass.oldpassword, updatepass.newpassword):
            user_request = get_user_by_id(updatepass.id)
            request = 'Update Successfull'

    return { "data": { 
                "request" :request,
                "user": user_request
                }
            }
    
   
