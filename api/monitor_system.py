from datetime import datetime
from main import app
from monitor_system.check_ML_model_metrics import *
from datetime import date as date_type

# @app.get('/monitor-num-distraction')
# def monitor_num_distraction(date: date_type):
#     # print('get')
#     monitor_percentage_of_distraction(date)
#     return {'percentage': 0}