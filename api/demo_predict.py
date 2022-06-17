from main import app
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from ML_model.predict import predict

@app.post("/demo_image")
def predict_image(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    # response_image.show()
    print('call')
    bbox, class_name, prob = predict(original_image)

    response_image = original_image
            #draw
    draw = ImageDraw.Draw(response_image) 
    text_location = [0, 0]
    if bbox is not None:
        draw.rectangle(bbox, outline ="red")

        text_location = [bbox[0] + 2., bbox[1] +1]
  
    draw.text(xy=text_location, text='{}, {:.2f}'.format(class_name, prob), fill='red', 
            font= ImageFont.truetype("arial.ttf", 30))

    # filtered_image = BytesIO()
    # original_image.save(filtered_image, "JPEG")
    # filtered_image.seek(0)
    filtered_image = BytesIO()
    response_image.save(filtered_image, "JPEG")
    filtered_image.seek(0)
    return StreamingResponse(filtered_image, media_type="image/jpeg")
    # return {'text': 'success'}
    # return {
    #     'bbox': bbox, 
    #     'class_name': class_name,
    #     'probability': float(prob)
    # }