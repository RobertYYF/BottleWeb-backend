from sqlalchemy import Column, Integer, Sequence, String
from config.db_config import base

class UserTable(base):
    __tablename__ = 'sys_user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(255))
    user_role = Column(String(10))
    