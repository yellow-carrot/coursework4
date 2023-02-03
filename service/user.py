import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_by_name(self, name):
        return self.dao.get_by_name(name)

    def get_user_by_email(self, email):
        return self.get_user_by_email(email)

    def get_all(self, filters):
        return self.dao.get_all(filters)

    def create(self, user_d):
        user_d['password'] = self.create_pwd_hash(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, user_d):

        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    def create_pwd_hash(self, password):

        hashed_pwd = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hashed_pwd)

    def compare_pwds(self, hashed_pwd, clear_pwd) -> bool:
        return hmac.compare_digest(
            base64.b64decode(hashed_pwd),
            hashlib.pbkdf2_hmac(
                'sha256',
                clear_pwd.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )

