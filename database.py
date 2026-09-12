from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)

class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Right Eye Metrics (OD)
    od_sph = Column(Float, nullable=True)
    od_cyl = Column(Float, nullable=True)
    
    # Left Eye Metrics (OS)
    os_sph = Column(Float, nullable=True)
    os_cyl = Column(Float, nullable=True)

# Using SQLite locally inside VS Code for immediate local testing
DATABASE_URL = "sqlite:///./optical.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)