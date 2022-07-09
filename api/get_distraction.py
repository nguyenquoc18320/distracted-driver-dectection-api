from datetime import date as date_type
from main import app
from auth.auth_handler import *
from fastapi import Depends, HTTPException
from auth.auth_bearer import JWTBearer
from services.user import *
from services.distraction import *


# get total distraction in a day
@app.get('/get-total-distraction')
def getTotalDistraction(userid: int, date: date_type, token: str = Depends(JWTBearer())):
    # get user

    current_userid = decodeJWT(token)['user_id']

    if current_userid != userid and check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # user = get_user_by_id(userid)

    # if user is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    # get account
    account = get_account_by_userid(userid)

    if account is None or account.status == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total = get_total_distraction_by_user(userid, date)

    if total is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"total": total}


# GET ALL number of distraction (admin role)
@app.get("/get-total-distraction-for-all")
def getTotalDistractionForAll(date: date_type, token: str = Depends(JWTBearer())):
    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    num_distraction = get_total_distraction(date)

    if num_distraction is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"total": num_distraction}


#get statistic of distractions, num_distractions are arranged desc,
# using pagination 
@app.get('/get-statistic-distraction')
def getStatisticDistraction(date: date_type, page: int, items_per_page: int,
                             token: str = Depends(JWTBearer())):
    if check_admin_role_by_token(token) == False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if page < 1:
        return {"data": [],
                "total_pages": 0}

    result, num_pages = get_num_distraction_for_each_user(
        date, page, items_per_page)

    #error processing
    if result is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"data": result,
            "page": page,
            "total_pages": num_pages}
