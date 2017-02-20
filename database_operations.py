from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class ClListing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'craigslist'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    title = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    metro_stop = Column(String)

class KjListing(Base):
    """
    A table to store data on kjiji listings.
    """

    __tablename__ = 'kijiji'

    id = Column(String, primary_key=True)
    link = Column(String, unique=True)
    price = Column(String)
    title = Column(String)
    address = Column(String)

def create_sqlite_session():
  engine = create_engine('sqlite:///listings.db', echo=False)
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  return session
