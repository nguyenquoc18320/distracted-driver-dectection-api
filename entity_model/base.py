from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:nguyenanhquoc1@localhost:3306/distracted_driver')

try:
    engine.connect()
    print('Connect successfully')
except:
    print('Cannot connect to database')
    
Session = sessionmaker(bind=engine)

Base = declarative_base()