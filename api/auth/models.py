from sqlalchemy import Column, String
from database.connection import Base

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = self.hash_password(password)  # Call hashing function

    def hash_password(self, password):
        # Import Passlib for secure password hashing
        from passlib.hash import bcrypt
        return bcrypt.hash(password)
