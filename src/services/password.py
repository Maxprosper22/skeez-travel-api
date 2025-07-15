from passlib.context import CryptContext

class PasswordService:
    # Initialize bcrypt context
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # @staticmethod
    # def make_hash(pwd):
    #     p_word = pwd.encode('utf-8')
    #     pwd_hash = hashlib.sha256(p_word)
    #     return pwd_hash
    #
    # @staticmethod
    # def verify(pwd, hashedpass):
    #     if self.make_hash(pwd) == hashedpass:
    #         return True
    #     else:
    #         return False
