from sqlalchemy import select
from entity_model.account import Account
from entity_model.user import User
from entity_model.role import Role
from entity_model.base import Base, engine, Session
import datetime
from sqlalchemy.orm import sessionmaker

def get_user_by_username_password(username: str, password: str) -> User:
    session = Session()
    acc_result = session.query(Account).filter(Account.username ==  username) \
                                        .filter(Account.password == password)
    session.close()
    
    for row in acc_result:
        return get_user_by_id(row.user.id)
    
    return None
def add_user2(names: str, driver_licenses: str)-> User:
    
    session = Session()
    user_new = User(name = names, gender = True, birthday =  datetime.datetime(2022, 1,1), phone='', driver_license = driver_licenses, role = get_role_by_id(1))
    current_user = session.merge(user_new)
    session.add(current_user)
    session.commit()
    session.close()

    return user_new

def add_user(names: str, driver_licenses: str, usernames: str, passwords: str)-> User:

    user_new = User(name = names, gender = True, birthday =  datetime.datetime(2022, 1,1), phone='', driver_license = driver_licenses, role = get_role_by_id(1))
    
    session = Session()
    current_user = session.merge(user_new)
    session.add(current_user)
    session.commit()
      
    session.expire(current_user)

    session.refresh(current_user)
    account_new = Account(username=usernames, password=passwords, user=get_user_by_license(driver_licenses))
    current_account = session.merge(account_new)
    session.add(current_account)
    session.commit()
    session.close()
    return user_new

def get_role_by_id (id) -> Role:
    session = Session()
    role_result = session.query(Role).filter(Role.id ==  id)
    session.close()
    
    for row in role_result:
        return row
    
    return None

def get_user_by_id (id) -> User:
    session = Session()
    user_result = session.query(User).filter(User.id ==  id)
    session.close()
    
    for row in user_result:
        return row
    
    return None

def get_user_by_license (driverlicense) -> User:
    session = Session()
    user_result = session.query(User).filter(User.driver_license ==  driverlicense)
    session.close()
    
    for row in user_result:
        return row
    
    return None

#---get all user 
def get_user_list() -> list():
    # try:
        user_list =[]
        session = Session()
        result = session.query(User).filter(User.role_id ==  2)
        session.close()
        print('done')
        for row in result:
            user_list.append(row)
        return user_list
    # except:
    #     print('error get users')
    #     return []