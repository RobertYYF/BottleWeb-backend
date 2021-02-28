from bottle import request, post, get, put, delete
from model.user import User

@get('/register')
def get_userguide():
    return {"userguide": "___user_guide___"}

@post('/register')
def add_user(db):
    data = request.json
    user = User()
    res = user.validate_register(db, data.get("username"), data.get("password"), data.get("user_role"))
    return {"res": res}


    