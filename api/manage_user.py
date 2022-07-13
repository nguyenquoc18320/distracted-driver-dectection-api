from fastapi import HTTPException
from main import app
from auth.auth_handler import *
from fastapi import FastAPI, Body, Depends
from auth.auth_bearer import JWTBearer
from services.user import *
from typing import List
from auth.auth_handler import check_admin_role_by_token

@app.get('/get-users')
def get_users_by_Admin_role (token: str = Depends(JWTBearer())):

    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    #--
    user_list = get_user_list()

    return { 
            'data':user_list
        }

@app.patch("/activate-user")
def activate_user(accountid: int, token: str = Depends(JWTBearer())):
        #check admin role
    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    #--activate
    result = activate_account(accountid)
    return {"data" : result}


@app.patch("/deactivate-user")
def deactivate_user(accountid: int, token: str = Depends(JWTBearer())):
    #check admin role
    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    #--activate
    result = deactivate_account(accountid)
    return {"data" : result}

