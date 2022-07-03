from fastapi import FastAPI, Body, Depends
from main import app
from auth.auth_bearer import JWTBearer
from datetime import date as date_type

from services.total_images import add_num_image

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def test_jwt(name: str) -> dict:
    # post.id = len(posts) + 1
    # posts.append(post.dict())
    return {
        "data": "post added."
    }

# @app.get("/test")
# async def test_jwt(userid: int, date:date_type):
#     add_num_image(userid, date)
#     return {
#         "data": "post added."
#     }