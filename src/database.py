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

    def get_user(self) -> dict:
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

    def add_user(self, name: str, user_ip: str) -> str:
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

    def get_invite(self, code: str) -> list:
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

    def find_user_chats(self) -> list:
        try:
            self.cursor.execute(
                'select chat_id from chat_member where user_token = %(token)s',
                {'token': self.token},
            )
            result = self.cursor.fetchall()
            self.finish()
            return result

        except Exception as e:
            logging.debug(e)

    def add_chat(self, name: str, description: str = None) -> dict or None:
        try:
            self.cursor.execute(
                'insert into chats(owner, name, description) values '
                '(%(owner)s, %(name)s, %(description)s) RETURNING id, name',
                {
                    'owner': self.token,
                    'name': name,
                    'description': description,
                }
            )
            self.conn.commit()
            result = self.cursor.fetchone()
            self.finish()
            return result

        except Exception as e:
            logging.warning(e)

    def get_chat(self, chat_id: int = None) -> bool:
        try:
            if not chat_id:
                self.cursor.execute(
                    'select id, name, description, last_message from chats where owner = %(token)s',
                    {'token': self.token},
                )
            else:
                self.cursor.execute(
                    'select id, name, description, last_message from chats where id = %(chat_id)s',
                    {'chat_id': chat_id},
                )
            result = self.cursor.fetchone()
            self.finish()
            return result

        except Exception as e:
            logging.debug(e)

    def add_member(self, user_id: int, chat_id: int) -> bool:
        try:
            self.cursor.execute(
                'insert into chat_member(user_id, chat_id) values '
                '(%(user_id)s, %(chat_id)s)',
                {
                    'user_id': user_id,
                    'chat_id': chat_id,
                }
            )
            self.conn.commit()
            self.finish()
            return True

        except Exception as e:
            logging.warning(e)

    def get_chats(self, user_id: int = None) -> list:
        try:
            if not user_id:
                user_id = PostgreSQL(self.token).get_user()["id"]
            self.cursor.execute(
                'select chat_id from chat_member where user_id = %(user_id)s',
                {
                    'user_id': user_id,
                }
            )
            result = self.cursor.fetchall()
            self.finish()
            return [i[0] for i in result]

        except Exception as e:
            logging.warning(e)
