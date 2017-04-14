#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))





class New_Post(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("new_post.html")
        content= t.render()
        self.response.write(content)
    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("blog_post")

        if  (not title == "") and (not blog_post ==""):
            blog_obj = Blog_Post(title = title, blog_post=blog_post)
            blog_obj.put()
            self.redirect("/"+str(blog_obj.key().id()))
        else:
            error = cgi.escape("Enter a title and post content before submitting", quote = True)
            t = jinja_env.get_template("new_post.html")
            content= t.render(error=error)
            self.response.write(content)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Blog_Post ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("blog.html")

        content= t.render(blog_posts = posts)
        self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):

        post = Blog_Post.get_by_id( int(id) )
        t = jinja_env.get_template("single_post.html")
        content= t.render(post = post)
        self.response.write(content)

class BlogHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/")


class Blog_Post(db.Model):
    title = db.StringProperty(required= True)
    blog_post = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new_post', New_Post),
    ('/blog', BlogHandler),
    webapp2.Route('/<id:\d+>', ViewPostHandler)
], debug=True)
