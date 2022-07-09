from datetime import datetime
from pickle import FALSE, TRUE
from tabnanny import check
from unittest import result
from fastapi import HTTPException
from auth.auth_handler import decodeJWT
from main import app
from fastapi import FastAPI, File, UploadFile, Depends,Form
from PIL import Image
from ML_model.predict import predict
from auth.auth_bearer import JWTBearer
from services.predict import add_distrac, add_no_person
from pydantic import BaseModel
import os
import random


from services.total_images import add_num_image
from services.user import get_account_by_userid
class New_Distraction(BaseModel):
    userid: int

@app.post("/add-distraction")
def add_distraction(img: UploadFile = File(...),  token: str = Depends(JWTBearer())):

    userid = decodeJWT(token)['user_id']
    account = get_account_by_userid(userid)

    if account is None or account.status==False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    original_image = Image.open(img.file)
    # original_image.show()
    print('save')
    dest_folder = 'images/distraction'
    if(os.path.exists(dest_folder) == False): 
            os.mkdir(dest_folder)
            
    now =datetime.now()
    img_name=  str(userid) + "_" + now.strftime("%Y_%m_%d_%H_%M_%S_%f") + "." + img.filename.split('.')[-1]
    # print(img_name)
    original_image.save(dest_folder + "/" + img_name) 
    bbox, class_name, prob = predict(original_image)

    #not detect person
    if bbox is None:
        print('h1')
        result_distrac = add_no_person(class_name, dest_folder + "/" +img_name, userid)
    else:
        print('h2')
        result_distrac = add_distrac(class_name, dest_folder + "/" + img_name,userid)
    if result_distrac is None:
            print('err1')
            raise HTTPException(status_code=500, detail="Internal Server Error")

    #add image
    result = add_num_image(userid=userid, date=datetime.now().date())

    if result is None:
        print('err2')
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return{
            "distraction": result_distrac
    }
    