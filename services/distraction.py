from datetime import datetime, date as date_type
from main import app
from auth.auth_handler import *
from fastapi import Depends, HTTPException
from auth.auth_bearer import JWTBearer
from services.user import *
from entity_model.distraction import Distraction


def get_total_distraction_by_user(userid, date: datetime):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.user_id == userid)\
                .filter(Distraction.no_person==False)\
                .filter(Distraction.time.between(start_day, end_day)).count()
        return result
    except:
        return None


def get_total_distraction(date: datetime):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.no_person==False)\
                .filter(Distraction.time.between(start_day, end_day)).count()
        return result
    except:
        return None

def get_total_image_not_detecting_person(date: datetime):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.no_person==True)\
                .filter(Distraction.time.between(start_day, end_day)).count()
        return result
    except:
        return None

def get_distraction_list(userid: int) -> list():
    # print("a")
    try:
        distraction_list =[]
        session = Session()
        # result = session.query(User).filter(User.role_id ==  2)
        result = session.query(Distraction).filter(Distraction.user  == get_user_by_id(userid))
        session.close()
        for row in result:

            distraction_list.append(row)
        print(distraction_list)
        return distraction_list
    except:
        print('error get distractions')
        return []
