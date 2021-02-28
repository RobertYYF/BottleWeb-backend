from model.tables import UserTable

# Database Utils

def insert(db, name, pwd, role):
    new_user = UserTable(username=name, password=pwd, user_role=role)
    db.add(new_user)
    db.commit()

def select_by_username(db, target_name):
    table_data = db.query(UserTable).filter(UserTable.username==target_name).first()
    if table_data == None:
        return None
    res = {"username": table_data.username, "password": table_data.password, "user_role": table_data.user_role}
    return res

def delete_by_username(db, target_name):
    target = db.query(UserTable).filter(UserTable.username==target_name)
    target.delete()

def update_password(db, username, pwd):
    db.query(UserTable).\
       filter(UserTable.username == username).\
       update({"password": pwd})
    db.commit()






