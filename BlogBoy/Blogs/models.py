from Config.service_app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime

class Blogs(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    title = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'category': self.category,
            'body': self.body
        }

    @classmethod
    def serialize(self, blogs):
        final = []
        for blog in blogs:
            blog_object = Blogs(id=blog.id)
            final.append(blog_object.to_dict())
        return final
