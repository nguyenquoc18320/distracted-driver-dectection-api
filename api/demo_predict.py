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

@app.post("/demo_image")
def predict_image(img: UploadFile = File(...)):
    try:    
        original_image = Image.open(img.file)
        # response_image.show()
        print('call')
        bbox, class_name, prob = predict(original_image)

        response_image = original_image
                #draw
        draw = ImageDraw.Draw(response_image) 
        text_location = [0, 0]

        text_size = 30 #for 640x480 image
        w, h = original_image.size
        text_size = int(text_size * (w/640))

        if bbox is not None:
            draw.rectangle(bbox, outline ="red", width=3)

            text_location = [bbox[0] + 2., bbox[1] +1]
    
        draw.text(xy=text_location, text='{}, {:.2f}'.format(class_name, prob), fill='red', 
                font= ImageFont.truetype("arial.ttf", text_size))

        filtered_image = BytesIO()
        response_image.save(filtered_image, "JPEG")
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type="image/jpeg")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file

@app.post("/demo_video")
def predict_image(video: UploadFile = File(...)):
    skip_frame = 15

    tmp_path = save_upload_file_tmp(video)

    try:
        p= r"{}".format(tmp_path)
        cap = cv2.VideoCapture(p)
        # cap.release()

        ret, frame = cap.read()

        h_orginal, w_original, _ = frame.shape
        # print(orginal_input_size)

        out_video=cv2.VideoWriter('video_demo/demo.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                30//skip_frame, (w_original,h_orginal), isColor=True)
        
        count = 0;

        while ret :
            if count % skip_frame == 0:
                #detect person
                #detect bbox
                im_pil = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(im_pil)

                bbox, class_name, prob = predict(im_pil)

                text_location = [0, 0]

                text_size = 1
                w, h = im_pil.size

                if w>640:
                    text_size = int(text_size * (w/(640*1.5)))

                if bbox is not None:
                    if class_name.lower() != 'safe driving':
                        frame = cv2.rectangle(frame, 
                                            (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                                            (0, 0, 255),2)

                        frame = cv2.putText(frame, '{}, {:.2f}'.format(class_name, prob), 
                                        (int(bbox[0]), int(bbox[1]+60)), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 
                                            text_size, (0, 0, 255), 3, cv2.LINE_AA)
                                            
                    else:
                        frame = cv2.rectangle(frame, 
                                            (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                                            (0, 255, 0), 2)
                        frame = cv2.putText(frame, '{}, {:.2f}'.format(class_name, prob), 
                                        (int(bbox[0]), int(bbox[1]+60)), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 
                                            text_size, (0, 255, 0), 3, cv2.LINE_AA)
                else: 
                    frame = cv2.putText(frame, '{}, {:.2f}'.format(class_name, prob), 
                                    (10, 60), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 
                                        text_size, (0, 255, 0), 3, cv2.LINE_AA)
            
                # cv2.imshow('img', frame)
                # cv2.waitKey(0)
                out_video.write(frame)
            count +=1
            ret, frame = cap.read()
            # if count==60:
            #     break

        cap.release()
        out_video.release()
        
    finally:
        tmp_path.unlink() 
        headers = {
            'Accept-Ranges': 'bytes'
        }
        return StreamingResponse(open('video_demo/demo.mp4', mode="rb"), headers=headers,media_type="video/mp4")
        # if os.path.exists('video_demo/demo.mp4'):
        #     return FileResponse('video_demo/demo.mp4', media_type="video/mp4", filename='demo_video.mp4')
        
        raise HTTPException(status_code=500, detail="Internal Server Error")


