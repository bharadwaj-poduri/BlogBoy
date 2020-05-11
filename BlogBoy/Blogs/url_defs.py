from Config.service_app import api

from Blogs.resources import BlogResource, CommentResource, LikesResource

api.add_resource(BlogResource, '/blogresource')
api.add_resource(CommentResource, '/commentresource')
api.add_resource(LikesResource, '/likeresource')
