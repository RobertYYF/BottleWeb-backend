from sqlalchemy import create_engine, Column, Integer, Sequence, String
import bottle_sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration file
base = declarative_base()

# MySQL DB Connection
# Username: robert
# Password: 123456
# Database name: mydb
engine = create_engine('mysql://test1:Aa123456789!@localhost:3306/springdb')

# engine = create_engine('mysql://robert:123456@172.17.0.2:3306/mydb')

create_session = sessionmaker(bind=engine)

plugin = bottle_sqlalchemy.Plugin(
        engine,
        base.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
)


