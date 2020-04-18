from Config.service_app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime

class Blogs(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.Text, nullable=True)
    msg = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject': self.subject,
            'type': self.type,
            'msg': self.msg
        }
