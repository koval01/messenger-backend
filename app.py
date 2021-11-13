import logging
from time import time

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_restful import Resource, Api

import database
import filter
from auth import check_, check_invite
from messages import messages_dict

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self) -> None:
        return jsonify({'run': True})


class GetChats(Resource):
    def get(self, token: str) -> None:
        g.start = time()
        c = check_(token, g.start)

        if c == 8:
            data = database.PostgreSQL(token).get_chats()
            return jsonify({
                "ok": True, "chat_ids": data,
                "time": round(time() - g.start, 3),
            })

        else:
            return c


class GetMe(Resource):
    def get(self, token: str) -> None:
        g.start = time()
        c = check_(token, g.start)

        if c == 8:
            data = database.PostgreSQL(token).get_user()
            return jsonify({
                "ok": True, "name": data["name"], "last_activity": data["last_activity"],
                "last_ip": data["last_ip"], "ban": data["ban"], "id": data["id"],
                "time": round(time() - g.start, 3),
            })

        else:
            return c


class CreateUser(Resource):
    def get(self, invite_code: str, name: str) -> None:
        g.start = time()
        c = check_invite(invite_code, g.start)

        if c == 8:
            try:
                if name == filter.Init(name).wide():
                    x = database.PostgreSQL().add_user(name, request.remote_addr)
                    database.PostgreSQL().delete_invite(invite_code)
                    return jsonify({"ok": True, "token": x, "time": round(time() - g.start, 3)})
                return jsonify({
                    "ok": False,
                    "result": messages_dict["username_error"],
                    "time": round(time() - g.start, 3)
                })

            except Exception as e:
                logging.warning(e)
                return jsonify({
                    "ok": False,
                    "result": messages_dict["account_create_error"],
                    "time": round(time() - g.start, 3)
                })

        else:
            return c


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
                                "result": messages_dict["chat_created"],
                                "chat_id": x["id"],
                                "chat_name": x["name"],
                                "time": round(time() - g.start, 3)
                            })

                    return jsonify({
                        "ok": False,
                        "result": messages_dict["chat_create_error"],
                        "time": round(time() - g.start, 3)
                    })

                return jsonify({
                    "ok": False, "result": messages_dict["chat_name_error"],
                    "time": round(time() - g.start, 3)
                })

            except Exception as e:
                logging.warning(e)
                return jsonify({
                    "ok": False,
                    "result": messages_dict["chat_create_error"],
                    "time": round(time() - g.start, 3)
                })

        else:
            return c


api.add_resource(status, '/')
api.add_resource(GetChats, '/chats/<token>/')
api.add_resource(GetMe, '/getme/<token>/')
api.add_resource(CreateUser, '/createuser/<invite_code>/<name>/')

api.add_resource(CreateChat, '/createchat/<token>/<name>/<description>/', '/createchat/<token>/<name>/')

if __name__ == '__main__':
    app.run()
