from bottle import get, post ,request
import model.user
import json

@post('/login')
def login_verify(db):
    data = request.json
    new_user = model.user.User()
    res = new_user.validate_login(db, data.get("username"), data.get("password"))
    if (res):
       token = new_user.generate_auth_token()
       user_role = new_user.get_user_role(db, data.get("username"))
       result = {"accessToken": str(token), "username": data.get("username"), "user_role": user_role}
       return json.dumps(result).encode("utf-8")
    else:
        return {}