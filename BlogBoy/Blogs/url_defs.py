from Config.service_app import api

from Blogs.resources import BlogResource, CommentResource

api.add_resource(BlogResource, '/blogresource')
api.add_resource(CommentResource, '/commentresource')
