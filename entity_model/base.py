from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql://root:nguyenanhquoc1@localhost:3306/distracted_driver')
engine = create_engine('mysql://root:nguyenanhquoc1@localhost:3306/distracted_driver', 
 pool_size=20, max_overflow=0, pool_recycle=60*60)
# engine = create_engine('mysql://root:123456@localhost:3306/distracted_driver2')
try:
    engine.connect()
    print('Connect successfully')
except:
    print('Cannot connect to database')
    
Session = sessionmaker(bind=engine)

Base = declarative_base()