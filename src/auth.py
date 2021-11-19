from time import time

from flask import jsonify

from src import database
from messages import messages_dict


def check_(token: str, start: float) -> int or jsonify:
    if database.PostgreSQL(token).get_user():
        return 8
    else:
        return jsonify({
            "ok": False, "result": messages_dict["auth_error"], "time": round(time() - start, 3)
        })


def check_invite(code: str, start: float) -> int or jsonify:
    if database.PostgreSQL().get_invite(code):
        return 8
    else:
        return jsonify({
            "ok": False, "result": messages_dict["invite_error"], "time": round(time() - start, 3)
        })
