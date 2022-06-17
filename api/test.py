from fastapi import FastAPI, Body, Depends
from main import app
from auth.auth_bearer import JWTBearer

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def test_jwt(name: str) -> dict:
    # post.id = len(posts) + 1
    # posts.append(post.dict())
    return {
        "data": "post added."
    }