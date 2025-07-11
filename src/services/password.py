import hashlib


class PasswordService:
    @staticmethod
    def make_hash(cls, pwd):
        p_word = pwd.encode('utf-8')
        my_hash = hashlib.sha256(p_word)
        return pw_hash
    
    @staticmethod
    def verify(cls, pwd, hashedpass):
        if self.make_hash(pwd) == hashedpass:
            return True
        else:
            return False
