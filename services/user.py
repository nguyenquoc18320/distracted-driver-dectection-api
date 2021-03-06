import math
from requests import session
from sqlalchemy import select, true, update
from xmlrpc.client import Boolean, DateTime, boolean
from torch import resize_as_sparse_
from entity_model.account import Account
from entity_model.user import User
from entity_model.base import Session
from  datetime import datetime
# from xmlrpc.client import Boolean, DateTime, boolean
from pickle import TRUE
from entity_model.role import Role

def get_user_by_username_password_for_login(username: str, password: str) -> User:
    session = Session()
    acc_result = session.query(Account).filter(Account.username ==  username) \
                                        .filter(Account.password == password)
    
    session.close()
    for row in acc_result:
        # check whether account is active
        if row.status == True:
            return get_user_by_id(row.user.id)
    return None

def add_user(names: str, driver_licenses: str, gender: bool, birthday: DateTime , phone: str, usernames: str, passwords: str)-> User:
    try:
        user_new = User(name = names, gender = gender, birthday =  birthday, phone=phone, driver_license = driver_licenses, role = get_role_by_id(2))
        
        session = Session()
        current_user = session.merge(user_new)
        session.add(current_user)
        session.commit()
        
        session.expire(current_user)

        session.refresh(current_user)
        account_new = Account(username=usernames, status=1, password=passwords, user=get_user_by_license(driver_licenses))
        current_account = session.merge(account_new)
        session.add(current_account)
        session.commit()
        session.close()
        return user_new
    except:
        return None

def update_user(id: int, name: str, gender: bool, birthday: DateTime , phone: str)-> User:
    try:
        session = Session()
        session.query(User).filter(User.id == id).update({'name': name, 'gender': gender, 'birthday': birthday, 'phone': phone})
        session.commit()
        session.close()
        
        return get_user_by_id(id)
    except:
        return None

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
    session.commit()
    session.close()
    
    for row in user_result:
        return row
    
    return None

def get_account_by_userid(userid) -> Account:
    session = Session()
    result = session.query(Account).filter(Account.user_id ==  userid) 
    session.commit()
    session.close()

    for row in result:
        return row
    
    return None

def get_user_by_id (id) -> User:
    session = Session()
    user_result = session.query(User).filter(User.id ==  id)
    session.commit()
    session.close()
    
    for row in user_result:
        return row
    
    return None

#---COUNT total users
def count_total_users() -> int:
    try:
        session = Session()
        # result = session.query(User).filter(User.role_id ==  2)
        result = session.query(User, Account).join(Account, User.id == Account.user_id)\
                    .filter(User.role_id==2).count()

        session.close()
        return result
        
    except:
        print('error get users')
        session.close()
        return 0

#---get all user 
def get_user_list(page, items_per_page) -> list():
    try:
        user_list =[]
        session = Session()
        # result = session.query(User).filter(User.role_id ==  2)
        result = session.query(User, Account).join(Account, User.id == Account.user_id)\
                    .filter(User.role_id==2)\
                    .order_by(User.name.asc())
                    
        all_num_users = result.count()
        #num pages for pagination
        num_pages = math.ceil(all_num_users/items_per_page)

        start_index = (page-1) * items_per_page 

        for row in result[start_index : (start_index + items_per_page)]:
            # hide username and password
            row['Account'].username = '******'
            row['Account'].password = '******'
            user_list.append(row)

        session.close()
        return user_list,  num_pages
    except:
        print('error get users')
        return []

#----ACTIVATE ACCOUNT
def activate_account(accountid: int) -> bool:
    '''Activate an account'''
    try:
        session =  Session()
        #get account
        acc_result = session.query(Account).filter(Account.id == accountid, Account.status == False)

        for row in acc_result:
            #deactivate the account
            result = session.query(Account).\
                    filter(Account.id == accountid, Account.status == False).\
                    update({'status': True})
            session.commit()
            
            session.close()
            if result > 0:
                return True

        session.close()
        return False
    except:
        session.close()
        return False


#---DEACTIVATE ACCOUNT
def deactivate_account(accountid: int) -> bool:
    '''Deactivate an account'''
    try:
        session =  Session()
        #get account
        acc_result = session.query(Account).filter(Account.id == accountid, Account.status == True)

        for row in acc_result:
            #deactivate the account
            result = session.query(Account).\
                    filter(Account.id == accountid, Account.status == True).\
                    update({'status': False})
            session.commit()
            
            session.close()
            if result > 0:
                return True

        session.close()
        return False
    except:
        session.close()
        return False

def get_account_by_license (driverlicense) -> Account:
    
    session = Session()
    user_result = session.query(Account).filter(Account.user == get_user_by_license(driverlicense))
    session.close()
    
    for row in user_result:
        return row
    
    return None
