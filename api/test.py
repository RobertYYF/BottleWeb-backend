from bottle import post, get, put, delete, request
from dao import user_dao

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





