import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_admin = Column(Integer, default=0)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    compactmode = Column(Integer, nullable=True)
    self_destruction_scale = Column(Integer, nullable=True)
    hope_scale = Column(Integer, nullable=True)
    mspss = Column(Integer, nullable=True)
    anxiety_scale = Column(Integer, nullable=True)
    depression_scale = Column(Integer, nullable=True)
    Fake_bad = Column(Integer, nullable=True)
    scales = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='results')

# Database Setup
class DBHelper:
    def __init__(self):
        self.engine = create_engine('sqlite:///quiz_app.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.create_default_admin()
        self.create_default_user()

    def create_default_admin(self):
        if not self.session.query(User).filter_by(username='admin').first():
            hashed_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
            admin = User(username='admin', password=hashed_password, is_admin=1)
            self.session.add(admin)
            self.session.commit()

    def create_default_user(self):
        if not self.session.query(User).filter_by(username='mahdi').first():
            hashed_password = bcrypt.hashpw("mahdi123".encode(), bcrypt.gensalt())
            user = User(username='mahdi', password=hashed_password, is_admin=0)
            self.session.add(user)
            self.session.commit()

    def fetch_users(self):
        return self.session.query(User).all()
    
    def validate_user(self, username: str, password: str):
        user = self.session.query(User).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode(), user.password):
            return user
        return None
    
    def insert_score(self, user_id, compactmode=0, self_destruction_scale=0, hope_scale=0, mspss=0, anxiety_scale=0, depression_scale=0, Fake_bad=0, scales=0):
        result = Result(user_id=user_id, compactmode=compactmode, self_destruction_scale=self_destruction_scale, hope_scale=hope_scale, mspss=mspss, anxiety_scale=anxiety_scale, depression_scale=depression_scale, Fake_bad=Fake_bad, scales=scales)
        self.session.add(result)
        self.session.commit()

    def show_full_name(self, user):
        return f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username
    
    def get_results_with_username(self):
        return self.session.query(Result, User.username).join(User, Result.user_id == User.id).all()