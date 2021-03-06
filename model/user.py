import hashlib
from dao import user_dao
from config.secure_config import SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

class User():
    def __init__(self):
        self.username = None
        self.password = None
    
    @staticmethod
    def salted_password(password, salt="`1234567890~!@#$%^&*()-=[];'\/,./ZXCVBNSADFYWQET"):
        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()

        # double encryption
        hash1 = md5hex(password)
        hash2 = md5hex(hash1 + salt)
        return hash2
    
    # Register
    def validate_register(self, db, username, pwd, role):
        if user_dao.select_by_username(db, username) is None:
            self.username = username
            user_dao.insert(db, username, self.salted_password(pwd), role)
            return True
        else:
            return False
    
    # Login
    def validate_login(self, db, username, pwd):
        temp = user_dao.select_by_username(db, username)
        if temp is not None:
            if (temp.get("password") == self.salted_password(pwd)):
                self.username = username
                return True
            else:
                return False

    # provide user role after login
    def get_user_role(self, db, username):
        temp = user_dao.select_by_username(db, username)
        if temp is not None:
            return temp.get("user_role")
        return None

    # Change password
    def change_pwd(self, db, username, form):
        # Different input password
        pwd1 = form.get("pwd1", "")
        pwd2 = form.get("pwd2", "")
        if pwd1 != pwd2:
            res = {
                "msg": "两次输入的旧密码不一样",
                "data": None
            }
            return res

        # Correct input pwd
        new_pwd = form.get("new_pwd", "")
        if self.salted_password(pwd1) == user_dao.select_by_username(db, username).get("password"):
            user_dao.update_password(db, username, self.salted_password(pwd1))
            res = {
                "msg": "Reset password success",
            }
        else:
            res = {
                "msg": "Incorrect old password",
            }
        return res

    # get new token，valid for 10min
    def generate_auth_token(self, expiration = 600):
        s = Serializer(SECRET_KEY, expires_in = expiration)
        print(self.username)
        return s.dumps({ 'id': self.username })

    # parse token for identification
    @staticmethod
    def verify_auth_token(token):
        print("start verifying token")
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("SignatureExpired")
            return None # valid token, but expired
        except BadSignature:
            print("BadSignature")
            return None # invalid token
        user = data['id']
        return user
