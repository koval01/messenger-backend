from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

from src.actions import *

app = Flask(__name__)
api = Api(app)
CORS(app)


api.add_resource(GetStatus, '/')
api.add_resource(GetChats, '/chats/<token>/')
api.add_resource(GetMe, '/getme/<token>/')

api.add_resource(CreateUser, '/createuser/<invite_code>/<name>/')
api.add_resource(CreateChat,
    '/createchat/<token>/<name>/<description>/',
    '/createchat/<token>/<name>/'
)

if __name__ == '__main__':
    app.run()
