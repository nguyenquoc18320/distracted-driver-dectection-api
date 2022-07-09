from main import app
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from ML_model.predict import predict
import cv2
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
import shutil
import os
import ntpath
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Get_image(BaseModel):
    img_path: str
@app.post("/get-image-imagepath")
def get_image(getimg: Get_image):
    try:    
        original_image = Image.open(getimg.img_path)
        # original_image.show()
        response_image = original_image
        ImageDraw.Draw(response_image) 
        filtered_image = BytesIO()
        response_image.save(filtered_image, "JPEG")
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type="image/jpeg")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
