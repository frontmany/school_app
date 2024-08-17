from ..extensions import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    student = db.Column(db.Integer)
    subject = db.Column(db.String(250))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    