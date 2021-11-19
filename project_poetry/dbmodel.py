from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Boolean
import os
import psycopg2

# CHANGE THIS SETTINGS IF YOU HAVE ANY DIFFERENT
DB_SCHEME = 'postgresql+psycopg2'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'
DB_SERVER = 'localhost'
DB_PORT = '5432'

# Not necessary to change
DB_NAME = 'lab6'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = '{}://{}:{}@{}:{}/{}'.format(
    DB_SCHEME,
    DB_USERNAME,
    DB_PASSWORD,
    DB_SERVER,
    DB_PORT,
    DB_NAME
)
engine = create_engine(connection_string, echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    name = Column(String(64), nullable=False)
    password = Column(String(500), nullable=False)
    role = Column(String(64))
    location_id = Column(Integer(),ForeignKey('location.id'))


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    title = Column(String(64))
    status = Column(Boolean,nullable=False)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    advertisement_id = Column(Integer(), ForeignKey('advertisement.id'), unique=True)
    text = Column(String(80), nullable=False, unique=True)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    city = Column(Integer())

class Advertisement_location(Base):
    __tablename__ = 'advertisement_location'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    location_id = Column(Integer(),ForeignKey('location_id'))
    advertisement_id =Column(Integer(),ForeignKey('advertisement_id'))

