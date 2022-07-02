from urllib import request
from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import get_account_by_license
from services.account import passwordreset
from pydantic import BaseModel

class Reset_Password(BaseModel):
    driver_license: str
    username: str
    newpassword: str
@app.put('/password_reset')
def password_reset(resetpass: Reset_Password):
    request = 'Fail'
    account_current = get_account_by_license(resetpass.driver_license)
    if account_current is None:
        request = 'Account does not exist!!!'
    else:
        if passwordreset(account_current, resetpass.username, resetpass.newpassword):
            request = 'Successfully'
    return { "data": { 
                "request" :request,
                }
            }
    
   
