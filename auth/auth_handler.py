import time
from typing import Dict

import jwt
from decouple import config

from services.user import get_user_by_id

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 60 * 60 * 24
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def check_admin_role_by_token(access_token: str ) -> bool:
    userid = decodeJWT(access_token)['user_id']

    #get user to make sure the user is admin
    user = get_user_by_id(userid)

    if user.role.name.lower() != 'admin':
        return False
    
    return True