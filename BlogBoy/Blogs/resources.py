from flask_restful import Resource
from flask import request
from UMS.models import Users
from BlogBoy.resources import BaseResource
from Blogs.models import Blogs, Comments
from flask import session
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.attributes import flag_modified
import json
from Config.service_app import app, db
from collections import defaultdict


class BlogResource(BaseResource):
    @jwt_required
    def post(self):
        data = request.get_json()
        category = data.get("category")
        title = data.get("title")
        body = data.get("body")
        if not session['user_id']:
            return self.json_response(success=False, error_message='Need to login in order to create a blog', error_code=400)

        new_blog = Blogs(
            user_id=session['user_id'],
            title=title,
            category=category,
            body=body
        )
        app.logger.info("new blog created: {}".format(new_blog.to_dict()))
        try:
            new_blog.save_to_db()
            data = new_blog.to_dict()
            return self.json_response(success=True, error_code=200, data=data)
        except Exception:
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)

    @jwt_required
    def get(self):
        category = request.args.get("category")
        id = request.args.get("id")
        user_id = request.args.get("user_id")
        title = request.args.get("title")
        data = None
        if id:
            data = Blogs.get_blog(id).to_dict()
        if user_id:
            blogs = Blogs.query.filter(Blogs.user_id == user_id).all()
            data = Blogs.serialize(blogs)
        if title:
            blogs = Blogs.query.filter(Blogs.title == title).all()
            data = Blogs.serialize(blogs)
        if category:
            blogs = Blogs.query.filter(Blogs.category == category).all()
            data = Blogs.serialize(blogs)
        return self.json_response(success=True, error_code=200, data=data)


class CommentResource(BaseResource):
    @jwt_required
    def post(self):
        if not session['user_id']:
            return self.json_response(success=False, error_message='Need to login in order to create a blog', error_code=400)

        data = request.get_json()
        user_id = session['user_id']
        blog_id = data.get('blog_id')
        body = data.get('body')
        parent = data.get('parent')

        if not Blogs.get_blog(blog_id):
            return self.json_response(success=False, error_message='Invalid blog id', error_code=400)

        comment = Comments(
            user_id = user_id,
            blog_id = blog_id,
            body = body,
            parent = parent if parent else -1
        )
        try:
            db.session.add(comment)
            app.logger.info("comment saved {}".format(comment.id))
            parent_comment = Comments.query.get(parent) if parent else Blogs.query.get(blog_id)
            if parent_comment.comments:
                parent_comment.comments.append(comment.id)
            else:
                parent_comment.comments = [comment.id]
            app.logger.info("comment saved in parent {}".format(parent_comment.comments))
            flag_modified(parent_comment, 'comments')
            db.session.commit()
            data = comment.to_dict()
            return self.json_response(success=True, error_code=200, data=data)
        except Exception:
            db.session.rollback()
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)

    @jwt_required
    def get(self):
        c_id = request.args.get('id')
        comment = Comments.get_comment(c_id).to_dict()
        child_comments = comment['comments'] if comment['comments'] else []
        comment_map = defaultdict()
        for comment_id in child_comments:
            comment_map[comment_id] = Comments.get_comment(comment_id).to_dict()
        comment['comments'] = comment_map
        return self.json_response(success=True, error_code=200, data=comment)


class LikesResource(BaseResource):
    @jwt_required
    def post(self):
        blog_id = request.args.get('blog_id')
        comment_id = request.args.get('comment_id')
        inc = request.args.get('inc')
        try:
            if blog_id:
                blog = Blogs.query.get(blog_id)
                blog.likes = blog.likes+1 if inc else (blog.likes-1 if blog.likes > 0 else 0)
                db.session.commit()
                data = {"likes": blog.likes, "blog_id": blog_id}
                return self.json_response(success=True, error_code=200, data=data)
            elif comment_id:
                comment = Comments.query.get(comment_id)
                comment.likes = comment.likes+1 if inc else (comment.likes-1 if comment.likes > 0 else 0)
                db.session.commit()
                data = {"likes": comment.likes, "comment_id": comment_id}
                return self.json_response(success=True, error_code=200, data=data)
            else:
                return self.json_response(success=True, error_code=400,
                                          data={"message": "No blog/comment with the given id"})
        except:
            db.session.rollback()
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)

    @jwt_required
    def get(self):
        blog_id = request.args.get('blog_id')
        comment_id = request.args.get('comment_id')
        if blog_id:
            blog = Blogs.query.get(blog_id)
            data = {"likes": blog.likes, "blog_id": blog_id}
            return self.json_response(success=True, error_code=200, data=data)
        elif comment_id:
            comment = Comments.query.get(comment_id)
            data = {"likes": comment.likes, "comment_id": comment_id}
            return self.json_response(success=True, error_code=200, data=data)
        else:
            return self.json_response(success=True, error_code=400,
                                      data={"message": "No blog/comment with the given id"})
