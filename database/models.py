from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database/store.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Float)
    status = Column(String)

Base.metadata.create_all(engine)
