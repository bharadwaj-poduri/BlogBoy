from Config.service_app import api

from Blogs.resources import BlogPost

api.add_resource(BlogPost, '/blogpost')
