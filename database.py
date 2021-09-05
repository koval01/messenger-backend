import logging
import psycopg2
from psycopg2 import extras
import generator

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER


class PostgreSQL:
    def __init__(self, token=None) -> None:
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASS, host=DB_HOST
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if token:
            self.token = token

    def finish(self) -> None:
        self.cursor.close()
        self.conn.close()

    def get_user(self) -> bool:
        try:
            self.cursor.execute(
                'select * from users where token = %(token)s',
                {'token': self.token},
            )
            result = self.cursor.fetchone()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def add_user(self, name, user_ip) -> str:
        token = generator.generate_token()
        self.cursor.execute(
            'insert into users(token, name, last_ip) values '
            '(%(token)s, %(name)s, %(last_ip)s)',
            {
                'token': token,
                'name': name,
                'last_ip': user_ip
            }
        )
        self.conn.commit()
        self.finish()
        return token

    def get_invite(self, code) -> list:
        try:
            self.cursor.execute(
                'select * from invite where invite_code = %(code)s',
                {'code': code},
            )
            result = self.cursor.fetchone()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def delete_invite(self, code: str) -> bool:
        try:
            self.cursor.execute(
                'delete from invite where invite_code = %(code)s',
                {'code': code},
            )
            self.conn.commit()
            self.finish()
            return True
        except Exception as e:
            logging.debug(e)
