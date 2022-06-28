from ML_model.SSD.SSD_predict_bbox import SSD_detect
from ML_model.recognition.recognition_predict import Recogition_model
from fastapi.responses import StreamingResponse
import numpy as np
import cv2

recognition_model = Recogition_model('ML_model/recognition/checkpoints/EfficientNetB0_new_flip-10-0.02.hdf5')

def predictimage(image):
    
    pil_image = image.convert('RGB')
    cv2_image = np.array(pil_image)
    cv2_image = cv2_image[:, :, ::-1].copy() 
        
    class_name, prob = recognition_model.recognize(cv2_image)
    print('{}, {}'.format(class_name, prob))
    
    return (class_name, prob)

