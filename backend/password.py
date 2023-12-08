from flask_bcrypt import Bcrypt

class PasswordManager:
    def __init__(self,app):
        self.app = app
        self.bcrypt = Bcrypt(app)

    def hash(self,password: str) -> str:
        return self.bcrypt.generate_password_hash(password).decode('utf-8')


    def check(self,hashed_password: str, password_to_check: str) -> bool:
        return self.bcrypt.check_password_hash(hashed_password, password_to_check)