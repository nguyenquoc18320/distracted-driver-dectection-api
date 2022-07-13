

# ---------Percentage of distraction----------
from datetime import datetime

from entity_model.base import Session
from entity_model.monitor_system import Monitor_system
from entity_model.total_images import Total_images
from monitor_system.send_email import send_mail
from services.distraction import get_total_distraction, get_total_image_not_detecting_person
from monitor_system.monitoring_threshold import *
#-----MONITOR PERCENTAGE of DISTRACTION (metrics =1)
# compute percentage of distraction per day
def monitor_percentage_of_distraction(date):
    session = Session()

    # only run monitoring func when date passed
    if date >= datetime.now().date():
        print('not day')
        session.close()
        return False

    # date was monitored
    result = session.query(Monitor_system).filter(
        Monitor_system.date==date).filter(Monitor_system.ml_metric_id == 1)
    for row in result:
        session.close()
        return False

    # get number of images sent on date
    result_total_image = session.query(
        Total_images.num_images).filter(Total_images.date == date)

    total_images = 0

    for row in result_total_image:
        total_images += row.num_images

    # no images sent on date
    if total_images != 0:
        # get num distraction
        total_distraction = get_total_distraction(date)

        if total_distraction is None:
            session.close()
            print('ERROR in ML monitor')
            return False

        percentage = float(total_distraction)/total_images
        print(percentage)

        if percentage > distraction_percentage:
            send_mail('nguyenquoc18320@gmail.com', 
            "ALERT from Distracted Driver Detection System\n" 
            + "Metric: distraction percentage"
            + "\nDate: " + date.strftime('%B %d, %Y') 
            + "\nThreshold: " + str(distraction_percentage)
            + "\nnCalculated PERCENTAGE: " + str(percentage)
            + "\n\nPlease evaluate ML system to make sure it works correctly!")


        monitoring_object = Monitor_system(id=0, date=date, statistic=percentage, ml_metric_id=1)
        session.add(monitoring_object)
        session.commit()
        session.close()
        print('monitor sucessfully')
        return True
    else:
        monitoring_object = Monitor_system(id=0, date=date, statistic=0, ml_metric_id=1)
        session.add(monitoring_object)
        session.commit()
        session.close()
        print('monitor sucessfully (0)')
        return True

#-----MONITOR PERCENTAGE of IMAGES Which SSD didn't detect person (metric=2)
def monitor_percentage_of_images_not_detect_person(date):
    session = Session()

    # only run monitoring func when date passed
    if date >= datetime.now().date():
        print('not day')
        session.close()
        return False

    # date was monitored
    result = session.query(Monitor_system).filter(
        Monitor_system.date==date).filter(Monitor_system.ml_metric_id == 2)
    for row in result:
        session.close()
        return False

    # get number of images sent on date
    result_total_image = session.query(
        Total_images.num_images).filter(Total_images.date == date)

    total_images = 0

    for row in result_total_image:
        total_images += row.num_images

    # no images sent on date
    if total_images != 0:
        # get num images not detected
        total_distraction = get_total_image_not_detecting_person(date)

        if total_distraction is None:
            session.close()
            print('ERROR in ML monitor')
            return False

        percentage = float(total_distraction)/total_images
        print(percentage)
        if percentage > not_recognize_person:
            send_mail('nguyenquoc18320@gmail.com', 
            "ALERT from Distracted Driver Detection System\n" 
            + "Metric: not recognizing person"
            + "\nDate: " + date.strftime('%B %d, %Y') 
            + "\nThreshold: " + str(not_recognize_person)
            + "\nCalculated PERCENTAGE: " + str(percentage) 
            + "\n\nPlease evaluate ML system (SSD) to make sure it works correctly!")

        monitoring_object = Monitor_system(id=0, date=date, statistic=percentage, ml_metric_id=2)
        session.add(monitoring_object)
        session.commit()
        session.close()
        print('monitor sucessfully')
        return True
    else:
        monitoring_object = Monitor_system(id=0, date=date, statistic=0, ml_metric_id=2)
        session.add(monitoring_object)
        session.commit()
        session.close()
        print('monitor sucessfully (0)')
        return True

