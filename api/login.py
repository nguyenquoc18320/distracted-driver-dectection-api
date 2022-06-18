from fastapi import HTTPException
from entity_model.account import Account
from entity_model.user import User
from main import app
from auth.auth_handler import *
from entity_model.base import Session
from entity_model.account import Account
from services.user import get_user_by_username_password
from pydantic import BaseModel


class Account(BaseModel):
    username: str
    password: str

@app.post('/login')
# def login (username: str, password: str):
def login (account: Account):
    result = get_user_by_username_password(account.username, account.password)

    if result is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = signJWT(result.id)

    return { "data": { 
                    "access_token" :token,
                    "user": result
                    }
            }



