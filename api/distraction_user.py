from datetime import date as date_type
from logging import NullHandler
from main import app
from auth.auth_handler import *
from fastapi import Depends, HTTPException, Form, Body
from auth.auth_bearer import JWTBearer
from services.user import *
from services.distraction import *
from pydantic import BaseModel
class UserBase(BaseModel):
    userid: int
@app.get('/getdistractions')
# def get_Distractions_by_user(userid: int = Body(...), token: str = Depends(JWTBearer())):
def get_distractions_by_userid(userid: int):#, token: str = Depends(JWTBearer())):
    # if check_admin_role_by_token(token) == False:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    #--
    distraction_list = get_distraction_list(userid)

    return { 
            'data':distraction_list
            
        }



@app.get('/get-list-distraction')
def get_distractions(userid: int, date: date_type, page: int, items_per_page: int, token: str = Depends(JWTBearer())):
    #check admin role
    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    list_result, num_page = get_distraction_list_by_pages(userid, date, page, items_per_page)
    return { 
            'data':list_result,
            'page': page,
            'total_pages': num_page
        }
