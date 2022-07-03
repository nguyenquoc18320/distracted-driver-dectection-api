from ML_model.SSD.SSD_predict_bbox import SSD_detect
from ML_model.recognition.recognition_predict import Recogition_model
from fastapi.responses import StreamingResponse
import numpy as np
import cv2

recognition_model = Recogition_model('ML_model/recognition/checkpoints/MobileNet_new_flip-15-0.01.hdf5',
                        threshold=0.7)

def predict(image):
    '''
    Detect driver and recognize driver's action
    image : read as PIL.Image
    Returns:
        bbox, class_name, probability
    '''
   
    bbox = SSD_detect(image)
    pil_image = image.convert('RGB')
    cv2_image = np.array(pil_image)
    # Convert RGB to BGR 
    cv2_image = cv2_image[:, :, ::-1].copy() 
    # cv2.imshow('img', cv2_image)
    # cv2.waitKey(0)

    if bbox is not None:
        bbox = [max(b, 0) for b in bbox] #(x1, y1, x2, y2)
        #make sure no bbox outside image
        bbox[2] = min(bbox[2], cv2_image.shape[1]-1)
        bbox[3] = min(bbox[3], cv2_image.shape[0]-1)
        cv2_image = cv2_image[int(bbox[1]) : int(bbox[3]), int(bbox[0]) : int(bbox[2]), :]
        
        class_name, prob = recognition_model.recognize(cv2_image)
        print('{}, {}'.format(class_name, prob))
    
        return (bbox, class_name, prob)
    
    #if not detecting person, return 'safe driving'
    print('safe driving, 0.5')
    return (None, 'safe driving', 0.5)
    # return StreamingResponse(filtered_image, media_type="image/jpeg")

