from Config.service_app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime
from collections import defaultdict


class Blogs(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    title = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.ARRAY(db.Integer), nullable=True)
    likes = db.Column(db.Integer, nullable=False, default=0)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        blog = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'category': self.category,
            'body': self.body,
            'likes': self.likes,
            'created_on': str(self.created_on),
            'updated_on': str(self.updated_on),
            'comments': self.comments
        }
        comments = blog['comments'] if blog['comments'] else []
        comment_map = defaultdict()
        for comment_id in comments:
            comment_map[comment_id] = Comments.get_comment(comment_id).to_dict()
        blog['comments'] = comment_map
        return blog

    @classmethod
    def serialize(cls, blogs):
        final = []
        for blog in blogs:
            final.append(blog.to_dict())
        return final

    @classmethod
    def get_blog(cls, id):
        return cls.query.filter(cls.id==id).first()


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, ForeignKey('blogs.id'), nullable=False)
    body = db.Column(db.Text, nullable=True)
    comments = db.Column(db.ARRAY(db.Integer), nullable=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    parent = db.Column(db.Integer, nullable=False, default=-1)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'blog_id': self.blog_id,
            'likes': self.likes,
            'body': self.body,
            'comments': self.comments,
            'created_on': str(self.created_on),
            'updated_on': str(self.updated_on)
        }

    @classmethod
    def get_comment(cls, id):
        return cls.query.filter(cls.id==id).first()