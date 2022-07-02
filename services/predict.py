from ML_model.SSD.SSD_predict_bbox import SSD_detect
from ML_model.recognition.recognition_predict import Recogition_model
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import os
import shutil
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from entity_model.base import Base, engine, Session
from entity_model.distraction import Distraction
from services.user import get_user_by_id

recognition_model = Recogition_model('ML_model/recognition/checkpoints/EfficientNetB0_new_flip-10-0.02.hdf5')

def predictimage(image):
    
    pil_image = image.convert('RGB')
    cv2_image = np.array(pil_image)
    cv2_image = cv2_image[:, :, ::-1].copy() 
        
    class_name, prob = recognition_model.recognize(cv2_image)
    print('{}, {}'.format(class_name, prob))
    
    return (class_name, prob)

def add_distrac(category, path, userid)-> Distraction:
    if get_distraction_by_pathimage(path) is None:
        
        new_Distrac = Distraction(time= datetime.now(), category= category, image_path= path, user=get_user_by_id(userid))
        session = Session()
        current_Distrac = session.merge(new_Distrac)
        session.add(current_Distrac)
        session.commit()
        session.close()
        return new_Distrac
    else:
        return None
def new_distraction(image) -> Distraction:
    print('add distrac')
    dest_folder = 'images/distraction'
    if(os.path.exists(dest_folder) == False): 
        os.mkdir(dest_folder)     
    with open(os.path.join(dest_folder,image.filename), "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return os.path.join(dest_folder,image.filename)
def get_distraction_by_pathimage (path) -> Distraction:
    session = Session()
    user_result = session.query(Distraction).filter(Distraction.image_path ==  path)
    session.close()
    
    for row in user_result:
        return row
    
    return None