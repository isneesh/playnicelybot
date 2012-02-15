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
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from playnicely.client import PlayNicely
from playnicely import AuthenticationError

HELP_MSG = ("/addme username##password \n"
            "/check \n"
            "/create newTask")
UNKNOWN_USER_MSG = "Do I know you? Please introduce yourself using /addme username##password"

class UnknownUserError(Exception):
    pass

class User(db.Model):
    user_name = db.TextProperty(required=True)
    password = db.TextProperty(required=True)

class XmppHandler(xmpp_handlers.CommandHandler):
    def _GetUser(self, sender):
        sender = sender.split('/')[0]
        user_k = db.Key.from_path('User',sender)
        user = db.get(user_k)
        if user == None : raise UnknownUserError
        return user

    def create_command(self, message=None):
        try :
            user = self._GetUser(message.sender)
        except UnknownUserError:
            message.reply(UNKNOWN_USER_MSG)
        else :
            text = message.arg
            client = PlayNicely(username = user.user_name, password = user.password)
            user_id = client.users.show("current").user_id
            item = client.items.create(project_id = 2512, subject=text, body="", responsible=1991, involved=[user_id, 1991], status="new",
                type_name="task", milestone_id=3)
            message.reply("Task " + str(item["item_id"]) + " created")


    def addme_command(self, message=None):
        sender = message.sender.split('/')[0]
        try:
            user_name, password = message.arg.split('##')
        except ValueError:
            message.reply("Incorrect format. Expected : \n/addme username##password")
        else :
            client = PlayNicely(username = user_name, password = password)
            try :
                current = client.users.show("current")
            except AuthenticationError as e:
                message.reply("Authentication failure, please try again ")
            else :
                user = User(key_name=sender, user_name=user_name, password=password)
                user.put()
                message.reply("Added successfully!")

    def check_command(self, message=None):
        try :
            user = self._GetUser(message.sender)
        except UnknownUserError:
            message.reply(UNKNOWN_USER_MSG)
        else :
            message.reply(user.user_name + "##" + user.password)

    def text_message(self, message=None):
        user = message.sender
        bare_jid = user.split('/')[0]
        message_text = message.arg
        message.reply(HELP_MSG)

def main():
    application = webapp.WSGIApplication([
        ('/_ah/xmpp/message/chat/', XmppHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
