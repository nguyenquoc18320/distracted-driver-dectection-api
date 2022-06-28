from sqlalchemy import select
from entity_model.account import Account
from entity_model.user import User
from entity_model.role import Role
from entity_model.base import Base, engine, Session
import datetime
from sqlalchemy.orm import sessionmaker

def add_account(usernames: str, passwords: str, users: User)-> Account:

    session = Session()
    account_new = Account(username=usernames, password=passwords, user=users)
    current_account = session.merge(account_new)
    session.add(current_account)
    session.commit()
    session.close()

    return account_new