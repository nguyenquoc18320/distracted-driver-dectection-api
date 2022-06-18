from sqlalchemy import select
from entity_model.account import Account
from entity_model.user import User
from entity_model.base import Session

def get_user_by_username_password(username: str, password: str) -> User:
    session = Session()
    acc_result = session.query(Account).filter(Account.username ==  username) \
                                        .filter(Account.password == password)
    session.close()
    
    for row in acc_result:
        return get_user_by_id(row.user.id)
    
    return None
    
def get_user_by_id (id) -> User:
    session = Session()
    user_result = session.query(User).filter(User.id ==  id)
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