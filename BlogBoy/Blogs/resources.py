from flask_restful import Resource
from flask import request
from UMS.models import Users
from Blogs.models import Blogs
from flask import session


class BlogPost(Resource):
    def post(self):
        data = request.get_json()
        typ = data.get("type")
        subject = data.get("subject")
        msg = data.get("msg")

        if not session['user_id']:
            return {'message': 'Need to login in order to create a blog'}

        new_blog = Blogs(
            user_id=session['user_id'],
            subject=subject,
            type=typ,
            msg=msg
        )
        print(new_blog.msg)
        try:
            new_blog.save_to_db()
            return new_blog.serialize()
        except Exception:
            return {'message' : 'Something went wrong'}

