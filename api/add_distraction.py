from unittest import result
from fastapi import HTTPException
from main import app
from fastapi import FastAPI, File, UploadFile, Depends,Form
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from ML_model.predict import predict
from services.predict import add_distrac
from pydantic import BaseModel
import os
class New_Distraction(BaseModel):
    userid: int

@app.post("/add-distraction")
def add_distraction(userid: int = Form(...), img: UploadFile = File(...)):
        original_image = Image.open(img.file)
        original_image.show()
        print('save')
        dest_folder = 'images/distraction'
        if(os.path.exists(dest_folder) == False): 
                os.mkdir(dest_folder)
                

        original_image.save(dest_folder + "/" + img.filename) 
        bbox, class_name, prob = predict(original_image)
        result_distrac = add_distrac(class_name, dest_folder + "/" + img.filename,userid)
        if result_distrac is None:
                raise HTTPException(status_code=401, detail="Unauthorized")
        return{
                "distraction": result_distrac
        }
    
