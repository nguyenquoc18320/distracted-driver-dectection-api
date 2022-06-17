import tensorflow.keras as keras
import cv2
import numpy as np
import tensorflow as tf

# #train with gpu
physical_devices = tf.config.experimental.list_physical_devices('GPU')
# print("GPU: ", physical_devices)
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

class Recogition_model():
    def __init__(self, model_path, input_image_size=(128, 128), threshold=0.5):
        self.model = keras.models.load_model(model_path)
        self.image_size = input_image_size
        self.threshold = threshold
        self.labels = self.get_label('ML_model/recognition/label_map.txt')

    
    def get_label(self, label_path):
        label={}
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                index = line.split(':')[0][1]
                name = line.split(':')[1][1:-1]
                label[int(index)] = name
        return label


    def preprocess(self, img):
        img = cv2.resize(img, self.image_size)

        return np.array(img, dtype = np.float32)

    def recognize(self, img):
        '''
        Recognize driver's action
        Returns:
            (class_name, probability)
        '''

        img = self.preprocess(img)

        pred = self.model.predict(np.array([img]))[0]

        pred_label = np.argmax(pred)
        prob = max(pred)
        
        if prob >= self.threshold:
            return self.labels[pred_label], prob
        else:
            return self.labels[0], 0.5


