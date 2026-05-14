import shelve
import hashlib
import os

class PasswordStore:
    def __init__(self,  master_key):
        self._db_file = 'user_passwords'
        self._master_key = master_key.encode('utf-8')

    def store_password(self, identifier, password):
        salt = os.urandom(16)
        pwd_bytes = password.encode('utf-8')
        key_stream = hashlib.pbkdf2_hmac('sha256', self._master_key, salt, 100000, len(pwd_bytes))
        encrypted = bytes(a ^ b for a, b in zip(pwd_bytes, key_stream))
        with shelve.open(self._db_file) as db:
            db[identifier] = salt + encrypted

    def retrieve_password(self, identifier):
        with shelve.open(self._db_file) as db:
            data = db.get(identifier)
            if not data:
                return None
        salt = data[:16]
        encrypted = data[16:]
        key_stream = hashlib.pbkdf2_hmac('sha256', self._master_key, salt, 100000, len(encrypted))
        decrypted = bytes(a ^ b for a, b in zip(encrypted, key_stream))
        return decrypted.decode('utf-8')

    def remove_password(self, identifier):
        with shelve.open(self._db_file) as db:
            if identifier in db:
                del db[identifier]

    def list_websites(self):
        with shelve.open(self._db_file) as db:
            return list(db.keys())
        


