from datetime import date as date_type
from main import app
from auth.auth_handler import *
from fastapi import Depends, HTTPException, Form, Body
from auth.auth_bearer import JWTBearer
from services.user import *
from services.distraction import *



# get total distraction in a day
@app.get('/get-total-distraction')
def getTotalDistraction(date: date_type, token: str = Depends(JWTBearer())):
    #get user
    userid = decodeJWT(token)['user_id']
    # user = get_user_by_id(userid)

    # if user is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    #get account
    account = get_account_by_userid(userid)

    if account is None or account.status==False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total = get_total_distraction_by_user(userid, date)

    if total is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"total": total}