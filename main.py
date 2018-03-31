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
import json
import logging
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# UserLogin function to be run on every page, so user can be logged in on every page
# and be able to add bookmarks and log out
def UserLogin(user_bookmarks_dict=bookmarks_dict):
    user = users.get_current_user()
    # if the user is logged in
    if user:
        nickname = user.nickname()
        global nickname
        # HTML to display username and sign out button
        logout_url = users.create_logout_url("/")
        greeting = "<p id='username' >Welcome, {}! <a id='login_link' href='{}'>Sign Out</a></p>".format(nickname, logout_url)
        # search DataStore for specific user, to see if this is their first login
        user_entity_query = UserProperties.query(UserProperties.username == nickname).fetch()
        # if list of user entities returned by query is empty (current user doesn"t exist), make new user entity
        if user_entity_query == []:
            # bookmarks made before logging in are added to the user"s list of bookmarks
            user_bookmarks_dict_json = json.dumps(user_bookmarks_dict)
            new_user = UserProperties(username=nickname, bookmarks=user_bookmarks_dict_json)
            new_user.put()
    # if no user logged in
    else:
        # HTML to display sign in button
        login_url = users.create_login_url("/")
        greeting = "<a id='login_link' href='{}'>Log in to save your Bookmarks!</a>.".format(login_url)
    # Dictionary to pass to template to display log in/out url
    login_dict = {"header": greeting}
    return login_dict

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
