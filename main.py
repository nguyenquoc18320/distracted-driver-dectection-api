from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from entity_model.create_db import *
from PIL import Image

app = FastAPI(debug=True)

@app.get("/")
def home():
    return {'text': 'Hello'}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#import all api
from api.login import *
from api.test import *
from api.demo_predict import *
from api.manage_user import *
from api.register import *
from api.password_reset import *
from api.change_pass import *
from api.update_user import *
from api.add_distraction import *
if __name__=='__main__':
    uvicorn.run(app)
    # image = Image.open('images\img_3.jpg')
    # predict(image)

