from datetime import datetime, date as date_type
from itertools import groupby

from cv2 import circle
from main import app
from auth.auth_handler import *
from fastapi import Depends, HTTPException
from auth.auth_bearer import JWTBearer
from services.user import *
from entity_model.distraction import Distraction
from sqlalchemy import func
from math import ceil

def get_total_distraction_by_user(userid, date: datetime):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.user_id == userid)\
            .filter(Distraction.no_person == False)\
            .filter(Distraction.time.between(start_day, end_day)).count()
        session.close()
        return result
    except:
        return None


def get_total_distraction(date: date_type):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.no_person == False)\
            .filter(Distraction.time.between(start_day, end_day)).count()
        session.close()
        return result
    except:
        return None


def get_total_image_not_detecting_person(date: datetime):
    try:
        session = Session()
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        result = session.query(Distraction).filter(Distraction.no_person == True)\
            .filter(Distraction.time.between(start_day, end_day)).count()
        session.close()
        return result
    except:
        return None


def get_num_distraction_for_each_user(date: datetime, page, items_per_page):
    try:
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59)

        session = Session()
        result_query = session.query(User,
                                    func.count(Distraction.id).label('num_distractions'))\
            .join(Distraction, User.id == Distraction.user_id)\
            .filter(Distraction.time.between(start_day, end_day))\
            .filter(Distraction.no_person==False)\
            .group_by(User.id)\
            .order_by(func.count(Distraction.id).label('num_distractions').desc())

        result = []
        all_num_record = result_query.count()
        #num pages for pagination
        num_pages = ceil(all_num_record/items_per_page)

        start_index = (page-1) * items_per_page 

        for row in result_query[ start_index : (start_index + items_per_page)]:
            data = {
                "User" : row["User"],
                "num_distractions": row['num_distractions']
            }
            result.append(data)
            # print(row['User'])

        session.close()
        return result, num_pages
    except:
        return None, None