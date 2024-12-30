from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///certification_assistant.db', echo=True)
Session = sessionmaker(bind=engine)
