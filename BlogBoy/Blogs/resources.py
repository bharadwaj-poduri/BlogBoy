from flask_restful import Resource
from flask import request
from UMS.models import Users
from Blogs.models import Blogs
from flask import session
from flask_jwt_extended import jwt_required


class BlogPost(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        category = data.get("category")
        title = data.get("title")
        body = data.get("body")

        if not session['user_id']:
            return {'message': 'Need to login in order to create a blog'}

        new_blog = Blogs(
            user_id=session['user_id'],
            title=title,
            category=category,
            body=body
        )
        print(new_blog.msg)
        try:
            new_blog.save_to_db()
            return new_blog.to_dict()
        except Exception:
            return {'message': 'Something went wrong'}

    @jwt_required
    def get(self):
        data = request.get_json()
        category = data.get("category")
        id = data.get("id")
        user_id = data.get("user_id")
        title = data.get("title")
        if id:
            return Blogs(id=id).serialize()
        if user_id:
            blogs = Blogs.query.filter(Blogs.user_id == user_id).all()
            return Blogs.serialize(blogs)
        if title:
            blogs = Blogs.query.filter(Blogs.title == title).all()
            return Blogs.serialize(blogs)
        if category:
            blogs = Blogs.query.filter(Blogs.category == category).all()
            return Blogs.serialize(blogs)
