# -*- coding: utf-8 -*-
import sys
sys.path.append("./model/")
from PIL import Image
from ML_model.SSD.utils import *
from torchvision import transforms
import torch
torch.cuda.empty_cache()
from ML_model.SSD.model.SSD300 import SSD300
from  ML_model.SSD.model.vgg import VGG16BaseNet, AuxiliaryNet, PredictionNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device='cpu'

trained_model = torch.load('model_state_ssd300.pth.tar', 
                map_location ='cpu')

start_epoch = trained_model["epoch"] + 1
print('\nLoaded model trained with epoch %d.\n' % start_epoch)
model = trained_model['model']
model = model.to(device)
model.eval()

resize = transforms.Resize((300, 300))
to_tensor = transforms.ToTensor()
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

def SSD_detect(original_image,min_score=0.4, 
                             max_overlap=0.45, top_k= 200, suppress = None):
    image = normalize(to_tensor(resize(original_image)))
    
    image = image.to(device)
    
    locs_pred, cls_pred = model(image.unsqueeze(0))
    
    detect_boxes, detect_labels, detect_scores = model.detect(locs_pred, cls_pred, 
                                                              min_score, max_overlap, top_k)
                                                        

    detect_boxes = detect_boxes[0].to('cpu')
    
    original_dims = torch.FloatTensor(
            [original_image.width, original_image.height, original_image.width, 
             original_image.height]).unsqueeze(0)
    
    detect_boxes = detect_boxes * original_dims
    
    detect_labels = [rev_label_map[l] for l in detect_labels[0].to('cpu').tolist()]
    
    box_location = None
    for i in range(detect_boxes.size(0)):
        if suppress is not None:
            if detect_labels[i] in suppress:
                continue

        if detect_labels[i] == 'person':
            box_location = detect_boxes[i].tolist()
            break
    return box_location
       

if __name__ == '__main__':
    img_path = 'images\img_3.jpg'
    original_image = Image.open(img_path, mode='r')
    original_image = original_image.convert('RGB')
    box_location = SSD_detect(original_image)
    print(box_location)
    # annotated_image.save(ouput_path)
    # annotated_image.show()