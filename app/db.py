from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engie = create_engine("mysql+pymysql://root:1234@localhost/tesis")
Session = sessionmaker(bind=engie)
session = Session()
Base = declarative_base()