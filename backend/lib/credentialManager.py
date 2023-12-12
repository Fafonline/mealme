from flask_bcrypt import Bcrypt
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CredentialManager:
    def __init__(self,app,credential_mgr):
        self.app = app
        self.bcrypt = Bcrypt(app)
        self.credential_mgr = credential_mgr

    def hash(self,password: str) -> str:
        return self.bcrypt.generate_password_hash(password).decode('utf-8')

    def check(self,hashed_password: str, password_to_check: str) -> bool:
        return self.bcrypt.check_password_hash(hashed_password, password_to_check)
    
# Function to verify user credentials
    def verify_credentials(self,username, password):
        user = self.credential_mgr.get_user(username)
        logger.info(f"User:{user}")
        try:
            stored_password = user.next().get('password', '')
            return self.check(stored_password, password)
        except  self.credential_mgr.not_found():
            return False