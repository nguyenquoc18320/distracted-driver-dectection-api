from xmlrpc.client import boolean
from sqlalchemy import select
from entity_model.account import Account
from entity_model.user import User
from entity_model.role import Role
from entity_model.base import Base, engine, Session
# import datetime
from sqlalchemy.orm import sessionmaker
from services.user import get_user_by_id
def add_account(usernames: str, passwords: str, users: User)-> Account:

    session = Session()
    account_new = Account(username=usernames, password=passwords, user=users)
    current_account = session.merge(account_new)
    session.add(current_account)
    session.commit()
    session.close()

    return account_new

def passwordreset(accountcurrent: Account, username_reset: str, newpassword: str) -> boolean:
    check = False
    if accountcurrent.username == username_reset:
        session = Session()
        session.query(Account).filter(Account.id == accountcurrent.id).update({'password': newpassword})
        session.commit()
        session.close()
        check = True
    return check

def get_account_by_user (userid: int) -> Account:
    
    session = Session()
    user_result = session.query(Account).filter(Account.user== get_user_by_id(userid))
    session.close()
    
    for row in user_result:
        return row
    
    return None

def passwordupdate(accountcurrent: Account, oldpassword: str, newpassword: str) -> boolean:
    check = False
    if accountcurrent.password == oldpassword:
        session = Session()
        session.query(Account).filter(Account.id == accountcurrent.id).update({'password': newpassword})
        session.commit()
        session.close()
        check = True
    return check