from msilib.schema import AdminExecuteSequence
import string
from fastapi import HTTPException
from main import app
from auth.auth_handler import *
from fastapi import FastAPI, Body, Depends
from auth.auth_bearer import JWTBearer
from services.user import *
from typing import List

@app.get('/get-users')
def get_users_by_Admin_role (token: str = Depends(JWTBearer())):
    userid = decodeJWT(token)['user_id']

    #get user to make sure the user is admin
    user = get_user_by_id(userid)

    if user.role.name.lower() != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")
        

    #--
    user_list = get_user_list()

    return { 
            'data':user_list
        }



