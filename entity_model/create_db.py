from entity_model.base import Base, engine, Session
from entity_model.role import Role
from entity_model.user import User
from entity_model.account import Account
# import datetime
from entity_model.distraction import Distraction
from entity_model.total_images import Total_images
from entity_model.ml_metric import ML_metric
from entity_model.monitor_system import Monitor_system

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - new session
session = Session()

# 4 - create records
# try:
#     admin_role = Role(1, 'admin')
#     driver_role = Role(2, 'driver')
#     session.add(admin_role)
#     session.add(driver_role)
# except:
#     print('err')
#     pass

# try:
        
#     user1 = User('Quoc', True, datetime.datetime(2022, 1,1), '0354316135', 'license1',driver_role)
#     account1 = Account('user1', '123456', True, user1)
#     session.add(user1)
#     session.add(account1)
    
#     distraction = Distraction(datetime.datetime(2022, 1,1, 12, 0, 0), 'drink', '/3', user1)
#     session.add(user1)
# except:
#     pass


# ###ML_metric
# try:
#     metric1 = ML_metric(1, 'Monitor percentage of distraction')
#     session.add(metric1)
    
#     metric2 = ML_metric(2, 'Monitor percentage of no person')
#     session.add(metric2)
# except:
#     pass

session.commit()
session.close()