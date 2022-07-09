from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from entity_model.create_db import *
from PIL import Image

app = FastAPI(debug=True)

@app.get("/")
def home():
    return {'text': 'Hello'}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# import all api

from api.monitor_system import *
from api.get_distraction import *
from api.login import *
from api.test import *
from api.demo_predict import *
from api.manage_user import *
from api.register import *
from api.password_reset import *
from api.change_pass import *
from api.update_user import *
from api.add_distraction import *
from api.distraction_user import *
from api.get_image import *
# ---AUTO MONITOR ML SYSTEM----

from datetime import datetime, timedelta
from monitor_system.check_ML_model_metrics import *
import threading
import time

class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        after_24_hours = False

        while True:
            # monitor system
            print('Checktime')
            if (datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
                    and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 2, 0, 0)):
                print('Run monitoring')
                monitor_day = datetime.now() - timedelta(days=1)
                monitor_percentage_of_distraction(monitor_day.date())
                monitor_percentage_of_images_not_detect_person(monitor_day.date())
                after_24_hours = True

            if after_24_hours:
                time.sleep(60 * 60 * 24)  # check again after 24 hours
            else:
                time.sleep(60 * 30)  # check agin after 30 minutes


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
