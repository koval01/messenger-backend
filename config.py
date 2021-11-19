import os

DB_HOST = os.environ.get("DB_HOST", None)
DB_NAME = os.environ.get("DB_NAME", None)
DB_USER = os.environ.get("DB_USER", None)
DB_PASS = os.environ.get("DB_PASS", None)

EMOJI = open("emoji.txt", "r").read()
