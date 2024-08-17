from ..extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from .post import Post 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    posts = db.relationship(Post, backref='author')
    name = db.Column(db.String(50))
    status = db.Column(db.String(50), default='user')
    login = db.Column(db.String(50))
    password = db.Column(db.String(250))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(250))
