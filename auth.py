from flask import jsonify
from time import time
import database


def check_(token: str, start: float) -> int or jsonify:
    if database.PostgreSQL(token).get_user():
        return 8
    else:
        return jsonify({"ok": False, "result": "Error auth check", "time": "%.5fs" % (time() - start)})


def check_invite(code: str, start: float) -> int or jsonify:
    if database.PostgreSQL().get_invite(code):
        return 8
    else:
        return jsonify({"ok": False, "result": "Error invite code check", "time": "%.5fs" % (time() - start)})
