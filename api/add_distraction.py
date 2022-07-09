from datetime import datetime
from pickle import FALSE, TRUE
from tabnanny import check
from unittest import result
from fastapi import HTTPException
from main import app
from fastapi import FastAPI, File, UploadFile, Depends,Form
from PIL import Image, ImageDraw, ImageFont
from ML_model.predict import predict
from services.predict import add_distrac, add_no_person
from pydantic import BaseModel
import os
import random


from services.total_images import add_num_image
class New_Distraction(BaseModel):
    userid: int

@app.post("/add-distraction")
def add_distraction(userid: int = Form(...), img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    # original_image.show()
    print('save')
    dest_folder = 'images/distraction'
    if(os.path.exists(dest_folder) == False): 
            os.mkdir(dest_folder)


    original_image.save(dest_folder + "/" + img.filename) 
    bbox, class_name, prob = predict(original_image)

    #not detect person
    if bbox is None:
        print('h1')
        result_distrac = add_no_person(class_name, dest_folder + "/" + img.filename, userid)
    else:
        print('h2')
        result_distrac = add_distrac(class_name, dest_folder + "/" + img.filename,userid)
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
    
    # while check_path is True: 
    #         i = 0
    #         for image_path in os.listdir(dest_folder):
    #             if image_path == img.filename:
    #                 print('h0')
    #                 img_path = str(random.randint(1, 100)) + '_' + img.filename
    #                 print(img_path)
    #                 i +=1
    #         if i == _change:
    #             check_path = FALSE