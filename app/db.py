from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engie = create_engine("mysql+pymysql://admin:tesis2022@database-1-tesis.cbzzayw2ryjl.us-east-1.rds.amazonaws.com/bd_tesis")
Session = sessionmaker(bind=engie)
session = Session()
Base = declarative_base()