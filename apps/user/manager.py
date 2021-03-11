import hashlib
import binascii

from django.db import models


class UserManager(models.Manager):
    def log_in(self, login_input):
        user = self.filter(email=login_input['email'])
        if user:
            user = user[0]
            hashed_input_pass = hashlib.pbkdf2_hmac('sha256',
                                                    login_input['password'].encode(),
                                                    binascii.hexlify(user.salt),
                                                    100000)
            if user.password == str(hashed_input_pass):
                return user
            return False

        else:
            return None

