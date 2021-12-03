import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from project_poetry.dbmodel import *
from schemas import *
from controller import *
import schemas
from controller import bcrypt

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# ======== User ========

def AddUser(userInfo):
    try:
        userInfo['password'] = bcrypt.generate_password_hash(userInfo['password'])
        session.add(Users(**userInfo))
        session.commit()
    except Exception as err:
        session.rollback()
        raise err


def Login(loginInfo):
    try:
        result = session.query(Users).filter_by(name=loginInfo['name']).first()
        if result == None:
            raise ValueError('No user found')
            if bcrypt.check_password_hash(result.password, loginInfo['password']) != True:
                raise ValueError('Incorrect password')
    except Exception as err:
        session.rollback()
        raise err


def Logout(login):
    try:
        print(login)
        result = session.query(Users).filter_by(name=login).first()
        if result == None:
            raise ValueError('No user found')
        print("Jopa")
        return result
    except Exception as err:
        raise err

def GetUserInfo(login):
    try:
        print(login)
        result = session.query(Users).filter_by(id=login).first()
        print(result['location_id'])
        location = session.query(LocationSchema).filter_by(id=result['location_id']).first()
        print(location)
        if result == None:
            raise ValueError('No user found')
        print("Jopa")
        result = schemas.UserSchema.dump(result)
        return result
    except Exception as err:
        session.rollback()
        raise err


def UpdateUserInfo(login, userInfo):
    try:
        isAny = session.query(Users).filter_by(name=login).first()
        if isAny == None:
            session.rollback()
            raise ValueError('No user found')
        if 'password' in userInfo:
            userInfo['password'] = bcrypt.generate_password_hash(userInfo['password'])
            session.query(Users).filter_by(name=login).update(userInfo)
            session.commit()
    except Exception as err:
        session.rollback()
        raise err


def deleteAdvertisement(id):
    try:
        print(id)
        ad = session.query(Message).filter_by(advertisement_id=id).all()
        print(ad is not None)
        if ad is not None:
            for ads in ad:
                session.delete(ads)
                session.commit
        advert = session.query(Advertisement).filter_by(id=id).first()
        print(advert is None)
        if advert is None:
            raise ValueError('Advertisement not found')
        session.delete(advert)
        session.commit
    except Exception as err:
        raise err

def DeleteUser(login):
    try:
        print(login)
        isAny = session.query(Users).filter_by(id=login).first()
        if isAny == None:
            session.rollback()
            raise ValueError('No user found')
        session.delete(isAny)
        session.commit()
    except Exception as err:
        session.rollback()
        raise err


def addAdvertisement(adverInfo):
    try:
        session.add(Advertisement(**adverInfo))
        session.commit()
    except Exception as err:
        session.rollback()
        raise err


def getAdvert(id):
    try:
        adver = session.query(Advertisement).filter_by(id=id).first()
        print(adver)
        if adver is None:
            raise ValueError('No advert found')
        message = session.query(Message).filter_by(advertisement_id=id).all()
        print(message)
        adver.message = message
        advertInfo = schemas.AdvertSchema().dump(adver)
        print(advertInfo)
        return advertInfo
    except Exception as err:
        session.rollback()
        raise err

def updateAdvert(id,advertInfo):
    try:
        isAny = session.query(Advertisement).filter_by(id=id).first()
        if isAny == None:
            session.rollback()
            raise ValueError('No advertisement found')
        else:
            session.query(Advertisement).filter_by(id=id).update(advertInfo)
            session.commit()
    except Exception as err:
        session.rollback()
        raise err

def deleteMessage(id):
    try:
        isAny = session.query(Message).filter_by(id=id).first()
        if isAny == None:
            session.rollback()
            raise ValueError('No message found')
        session.delete(isAny)
        session.commit()
    except Exception as err:
        session.rollback()
        raise err

def addMesage(messageInfo):
    try:
        isAdv = session.query(Advertisement).filter_by(id=messageInfo['advertisement_id']).first()
        if(isAdv == None):
            session.rollback()
            raise ValueError("No advertisement found for this message")
        session.add(Message(**messageInfo))
        session.commit()
    except Exception as err:
        session.rollback()
        raise err


def getPrivateAdvert(id, advList=None):
    try:
        user = session.query(Users).filter_by(id=id).first()
        print(user)
        if user == None:
            session.rollback()
            raise ValueError("User not found")
        list = session.query(Advertisement_location).filter_by(location_id=user.__dict__['location_id']).all()
        print(list)
        mass=[]
        index =0
        for lif in list:
            adverts =session.query(Advertisement).filter_by(id=lif.__dict__['advertisement_id']).first()
            if(adverts.__dict__['status'] == False):
                continue;
            adverts =schemas.AdvertSchema().dump(adverts)
            mass.append(adverts)
        if len(list) == 0:
            raise ValueError("You cant see advertisement")
        return mass
    except Exception as err:
        session.rollback()
        raise err

def getLocalAdvert(id, advList=None):
    try:
        user = session.query(Users).filter_by(id=id).first()
        print(user)
        if user == None:
            session.rollback()
            raise ValueError("User not found")
        list = session.query(Advertisement_location).filter_by(location_id=user.__dict__['location_id']).all()
        print(list)
        mass=[]
        index =0
        for lif in list:
            adverts =session.query(Advertisement).filter_by(id=lif.__dict__['advertisement_id']).first()
            if(adverts.__dict__['status'] == True):
                continue;
            adverts =schemas.AdvertSchema().dump(adverts)
            mass.append(adverts)
        if len(list) == 0:
            raise ValueError("You cant see advertisement")
        return mass
    except Exception as err:
        session.rollback()
        raise err