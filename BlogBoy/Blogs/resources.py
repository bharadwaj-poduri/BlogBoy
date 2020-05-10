from flask_restful import Resource
from flask import request
from UMS.models import Users
from Blogs.models import Blogs, Comments
from flask import session
from flask_jwt_extended import jwt_required
from Config.service_app import app
from sqlalchemy.orm.attributes import flag_modified
import json
from Config.service_app import app, db


class BlogResource(Resource):
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
        app.logger.info("new blog created: {}".format(new_blog.to_dict()))
        try:
            new_blog.save_to_db()
            return new_blog.to_dict()
        except Exception:
            return {'message': 'Something went wrong'}

    @jwt_required
    def get(self):
        category = request.args.get("category")
        id = request.args.get("id")
        user_id = request.args.get("user_id")
        title = request.args.get("title")
        if id:
            return Blogs.get_blog(id).to_dict()
        if user_id:
            blogs = Blogs.query.filter(Blogs.user_id == user_id).all()
            return Blogs.serialize(blogs)
        if title:
            blogs = Blogs.query.filter(Blogs.title == title).all()
            return Blogs.serialize(blogs)
        if category:
            blogs = Blogs.query.filter(Blogs.category == category).all()
            return Blogs.serialize(blogs)


class CommentResource(Resource):
    @jwt_required
    def post(self):
        if not session['user_id']:
            return {'message': 'Need to login in order to create a blog'}

        data = request.get_json()
        user_id = session['user_id']
        blog_id = data.get('blog_id')
        body = data.get('body')
        parent = data.get('parent')

        comment = Comments(
            user_id = user_id,
            blog_id = blog_id,
            body = body,
            parent = parent if parent else -1
        )
        try:
            comment.save_to_db()
            app.logger.info("comment saved {}".format(comment.id))
            parent_comment = Comments.query.get(parent) if parent else Blogs.query.get(blog_id)
            if parent_comment.comments:
                parent_comment.comments.append(comment.id)
            else:
                parent_comment.comments = [comment.id]
            app.logger.info("comment saved in parent {}".format(parent_comment.comments))
            flag_modified(parent_comment, 'comments')
            db.session.commit()
            return comment.to_dict()
        except Exception:
            db.session.rollback()
            return {'message': 'Something went wrong'}