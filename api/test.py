from bottle import post, get, put, delete, request, response
from dao import user_dao
from model.user import User

# api test

@get('/test')
def show(db):
    # results = user_dao.select_by_username(db, "robert")
    return {'table_data': "hello there"}

@post('/test/add')
def add_test(db):
    data = request.json
    user_dao.insert(db, data.get("username"), data.get("password"), data.get("user_role"))
    return {'result': "added"}

@post('/test/delete')
def delete_test(db):
    data = request.json
    user_dao.delete_by_username(db, data.get("username"))
    return {'result': "deleted"}

@post('/test/update')
def update_test(db):
    data = request.json
    user_dao.update_password(db, data.get("username"), data.get("password"))
    return {'result': "update success"}

# token test

# access public content without token
@get('/test/public')
def get_public_test():
    return {"content": "public content"}

# access private content with token
@get('/test/private')
def get_private_test():
    data = request.headers
    # verify token
    token = data['Authorization']
    token = bytes(token[2:len(token)-1], 'utf-8')
    print(token)
    username = User.verify_auth_token(token)
    # if token is valid, username will be returned
    if username != None:
        print(username)
        return {"content": "private content"}
    # invalid token
    else:
        return {"content": "ERROR"}




