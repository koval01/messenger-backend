import logging

from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api
from flask_cors import CORS
from auth import check_, check_invite
from time import time
import database
import filter

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self) -> None:
        g.start = time()
        return jsonify({'run': True, "time": "%.5fs" % (time() - g.start)})


class GetChats(Resource):
    def get(self, token: str) -> None:
        g.start = time()
        c = check_(token, g.start)
        if c == 8:
            data = database.PostgreSQL(token).get_chats()
            return jsonify({
                "ok": True, "chat_ids": data,
                "time": "%.5fs" % (time() - g.start),
            })
        else: return c


class GetMe(Resource):
    def get(self, token: str) -> None:
        g.start = time()
        c = check_(token, g.start)
        if c == 8:
            data = database.PostgreSQL(token).get_user()
            return jsonify({
                "ok": True, "name": data["name"], "last_activity": data["last_activity"],
                "last_ip": data["last_ip"], "ban": data["ban"], "id": data["id"],
                "time": "%.5fs" % (time() - g.start),
            })
        else: return c


class CreateUser(Resource):
    def get(self, invite_code: str, name: str) -> None:
        g.start = time()
        c = check_invite(invite_code, g.start)
        if c == 8:
            try:
                if name == filter.Init(name).wide():
                    x = database.PostgreSQL().add_user(name, request.remote_addr)
                    database.PostgreSQL().delete_invite(invite_code)
                    return jsonify({"ok": True, "token": x, "time": "%.5fs" % (time() - g.start)})
                return jsonify({
                    "ok": False,
                    "result": "The name can be Latin or Cyrillic characters, numbers and signs"
                              " \"-\" and \"_\" are also allowed. Also do not forget that at the "
                              "beginning and at the end of the term all indents are cut off, "
                              "therefore check up whether.",
                    "time": "%.5fs" % (time() - g.start)
                })
            except Exception as e:
                logging.warning(e)
                return jsonify({
                    "ok": False,
                    "result": "Error create account. The name may be longer than 255 characters.",
                    "time": "%.5fs" % (time() - g.start)
                })
        else: return c


class CreateChat(Resource):
    def get(self, token: str, name: str, description: str = "") -> None:
        g.start = time()
        c = check_(token, g.start)
        if c == 8:
            try:
                if name == filter.Init(name).wide() and \
                        description == filter.Init(description).default():
                    user_ = database.PostgreSQL(token).get_user()
                    x = database.PostgreSQL(token).add_chat(name, description)
                    if x and user_:
                        y = database.PostgreSQL(token).add_member(user_["id"], x["id"])
                        if y:
                            return jsonify({
                                "ok": True,
                                "result": "The group was successfully created",
                                "chat_id": x["id"],
                                "chat_name": x["name"],
                                "time": "%.5fs" % (time() - g.start)
                            })
                    return jsonify({
                        "ok": False,
                        "result": "Group create error",
                        "time": "%.5fs" % (time() - g.start)
                    })
                return jsonify({
                    "ok": False, "result": "The name can be Latin or Cyrillic characters, numbers and signs"
                                           " \"-\" and \"_\" are also allowed. All basic punctuation marks "
                                           "are allowed for the description. Also do not forget that at the "
                                           "beginning and at the end of the term all indents are cut off, "
                                           "therefore check up whether. The name or description may be "
                                           "longer than 255 characters.",
                    "time": "%.5fs" % (time() - g.start)
                })
            except Exception as e:
                logging.warning(e)
                return jsonify({
                    "ok": False,
                    "result": "Error create chat",
                    "time": "%.5fs" % (time() - g.start)
                })
        else: return c


api.add_resource(status, '/')
api.add_resource(GetChats, '/chats/<token>/')
api.add_resource(GetMe, '/getme/<token>/')
api.add_resource(CreateUser, '/createuser/<invite_code>/<name>/')

api.add_resource(CreateChat, '/createchat/<token>/<name>/<description>/', '/createchat/<token>/<name>/')

if __name__ == '__main__':
    app.run()
