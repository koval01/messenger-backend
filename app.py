from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api
from flask_cors import CORS
from auth import check_, check_invite
from time import time
import database
import re

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self):
        g.start = time()
        return jsonify({'run': True, "time": "%.5fs" % (time() - g.start)})


class GetChats(Resource):
    def get(self, token):
        g.start = time()
        c = check_(token, g.start)
        if c == 8:
            return jsonify({
                "ok": True, "data": database.PostgreSQL(token).get_user(),
                "time": "%.5fs" % (time() - g.start),
            })
        else: return c


class GetMe(Resource):
    def get(self, token):
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
    def get(self, invite_code, name):
        g.start = time()
        c = check_invite(invite_code, g.start)
        if c == 8:
            try:
                if name == re.sub(r"[^A-Za-z]", "", name):
                    x = database.PostgreSQL().add_user(name, request.remote_addr)
                    database.PostgreSQL().delete_invite(invite_code)
                    return jsonify({"ok": True, "token": x, "time": "%.5fs" % (time() - g.start)})
                return jsonify({"ok": False, "result": "The name can only consist of Latin letters", "time": "%.5fs" % (time() - g.start)})
            except Exception as e:
                return jsonify({
                    "ok": False, "result": "Error create account", "time": "%.5fs" % (time() - g.start)
                })
        else: return c


api.add_resource(status, '/')
api.add_resource(GetChats, '/chats/<token>/')
api.add_resource(GetMe, '/getme/<token>/')
api.add_resource(CreateUser, '/createuser/<invite_code>/<name>')

if __name__ == '__main__':
    app.run()
