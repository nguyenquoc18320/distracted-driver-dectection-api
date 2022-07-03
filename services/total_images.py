from sqlalchemy import true
from entity_model.base import Session
from entity_model.total_images import Total_images
from services.user import get_user_by_id


def add_num_image(userid, date):
    session = Session()

    #find total image record
    current_num_image =0
    result_total_image = session.query(Total_images)\
                                .filter(Total_images.user_id==userid)\
                                .filter(Total_images.date==date)

    for row in result_total_image:
        current_num_image = row.num_images

    if current_num_image!=0:
        #increase num images
        session.query(Total_images)\
                .filter(Total_images.user_id==userid)\
                .filter(Total_images.date==date)\
                .update({'num_images' : int(current_num_image) +1})
    else:
        #add new record
        result_total_image= Total_images(0, date, 1, user=get_user_by_id(userid))
        new_total_image = session.merge(result_total_image)
        session.add(new_total_image)


    session.commit()
    session.close()
    return True
