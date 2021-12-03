import bcrypt
from flask import Flask, request
from flask_bcrypt import Bcrypt
import schemas
import commands
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import sessionmaker
from project_poetry.dbmodel import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

Session = sessionmaker()
Session.configure(bind=engine)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login, password):
    session = Session()
    found_user = session.query(Users).filter_by(name=login).first()
    if not found_user:
        return False
    if Bcrypt().check_password_hash(found_user.password, password):
        return found_user


# ======== USER ========

@app.route('/users', methods=['POST'])
@auth.login_required
def userRoot():
    try:
        schema = schemas.UserSchema()
        data = request.json
        print(data)
        userInfo = schema.load(data)
    except ValidationError as err:
        return f'Validation error.\n{err}', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    try:
        commands.AddUser(userInfo)
    except IntegrityError as err:
        return f'User with the same email or login already exists', 403
    except Exception as err:
        return f'Internal server error. {err}', 500

    return f'User added successfully'


@app.route('/user/login', methods=['GET'])
def userLogin():
    try:
        schema = schemas.LoginSchema()
        data = request.json
        loginInfo = schema.load(data)
    except ValidationError as err:
        return f'Validation error.\n{err}', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    try:
        commands.Login(loginInfo)
    except ValueError as err:
        return f'Incorrect username / password', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    return 'Successful login!'


# CAN'T IMPLEMENT WITHOUT AUTH !!!
@app.route('/user/logout', methods=['GET'])
def userLogout():
    data = request.json
    login = data.pop('name', None)
    if login is None:
        return f'No login provided', 400
    try:
        schema = schemas.ValidateUserFieldsSchema().load({"name": login})
    except ValidationError as err:
        return f'{err}', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    try:
        userInfo = commands.Logout(login)
        displayValue = f'''
        Loggout successful
       '''
    except ValueError as err:
        return f'Uncorrected logout', 200
    except Exception as err:
        return f'Internal server error. {err}', 500
    return f'{displayValue}'


@app.route('/user/<login>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def userHandling(login):
    if request.method == 'GET':
        try:
            schema = schemas.ValidateUserFieldsSchema().load({"name": login})
        except ValidationError as err:
            return f'{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            print(login)
            userInfo = commands.GetUserInfo(login)
            displayValue = f'''
      name = {userInfo['name']}; 
      role = {userInfo['role']}; 
      location_id = {userInfo['location_id']}; 
      '''
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500
        return f'{displayValue}'

    elif request.method == 'PUT':
        userInfo = None
        try:
            schema = schemas.ValidateUserFieldsSchema()
            data = request.json
            userInfo = schema.load(data)
        except ValidationError as err:
            return f'Validation error.\n{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            print(login)
            commands.UpdateUserInfo(login, userInfo)
        except ValueError as err:
            return f'{err}', 404
        except IntegrityError as err:
            return f'Already exists', 403
        except Exception as err:
            return f'Internal server error. {err}', 500
        return f'Info changed successfully'

    elif request.method == 'DELETE':

        try:
            schema = schemas.ValidateMessageFieldsSchema().load({"id": login})
        except ValidationError as err:
            return f'{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            commands.DeleteUser(login)
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500
        return f'Deleted {login}'


@app.route('/advert', methods=['POST'])
@auth.login_required
def advertRoot():
    try:
        schema = schemas.AdvertSchema()
        data = request.json
        advertInfo = schema.load(data)
    except ValidationError as err:
        return f'Validation error.\n{err}', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    try:
        commands.addAdvertisement(advertInfo.copy())
    except Exception as err:
        return f'Internal server error. {err}', 500
    return f'{advertInfo}'


@app.route('/message/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def deleteMessage(id):
    if request.method == 'DELETE':
        try:
            schema = schemas.ValidateMessageFieldsSchema().load({"id": id})
        except ValidationError as err:
            return f'{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            commands.deleteMessage(id)
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500

        return f'Deleted {id}'



@app.route('/message', methods=['POST'])
def messageRoot():
    try:
        schema = schemas.MessageSchema()
        data = request.json
        messageInfo = schema.load(data)
    except ValidationError as err:
        return f'Validation error.\n{err}', 400
    except Exception as err:
        return f'Internal server error. {err}', 500

    try:
        commands.addMesage(messageInfo.copy())
    except Exception as err:
        return f'Internal server error. {err}', 500
    return f'{messageInfo}'


@app.route('/advert/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def advertHandling(id):
    if request.method == 'GET':
        try:
            schema = schemas.ValidateMessageFieldsSchema().load({"id": id})
        except ValidationError as err:
            return f'Not a valid integer', 400
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            advertInfo = commands.getAdvert(id)
            displayStudent = f'''
              title = {advertInfo['title']};
              status = {advertInfo['status']};
              message ={advertInfo['message']}
          '''
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500
        return f'{displayStudent}'
    elif request.method == 'PUT':
        advertInfo = None
        try:
            data = request.json
            print(data['title'])
            print(data['status'])
            schema = schemas.ValidateAdvertSchema()
            advertInfo = schema.load(data)
            print(advertInfo)
        except ValidationError as err:
            return f'Validation error.\n{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            commands.updateAdvert(id, advertInfo)
        except ValueError as err:
            return f'{err}', 404
        except IntegrityError as err:
            return f'Already exists', 403
        except Exception as err:
            return f'Internal server error. {err}', 500

        return f'Info changed successfully'
    elif request.method == 'DELETE':
        try:
             schema = schemas.ValidateMessageFieldsSchema().load({"id":id})
        except ValidationError as err:
            return f'{err}', 400
        except Exception as err:
            return f'Internal server error. {err}', 500

        try:
            commands.deleteAdvertisement(id)
        except ValueError as err:
            return f'{err}', 404
        except Exception as err:
            return f'Internal server error. {err}', 500

        return f'Deleted {id}'


@app.route('/listl/<top>', methods=['GET'])
def localAdvert(top):

    try:
        displayAdv = ""
        advertInfo = commands.getPrivateAdvert(top)
        for ad in advertInfo:
            displayAdv += f'''
                          title = {ad['title']};
                          status = false
                      '''
        return f'{displayAdv}'
    except Exception as err:
        return f'Internal server error. {err}', 500

@app.route('/listp/<top>', methods=['GET'])
@auth.login_required
def privateAdvert(top):

    try:
        displayAdv = ""
        advertInfo = commands.getLocalAdvert(top)
        for ad in advertInfo:
            displayAdv += f'''
                          title = {ad['title']};
                          status = {ad['status']}
                      '''
        return f'{displayAdv}'
    except Exception as err:
        return f'Internal server error. {err}', 500

if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
