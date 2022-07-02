from flask import request
from models.users import users


def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    if username and password:
        if [x for x in users if x["username"] == username and x["password"] == password]:
            return {}
        else:
            return {'msg': 'username or password is incorrect'}
    else:
        return {'msg': 'Missing username or password'}
