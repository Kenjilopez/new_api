from repository.users_repository import UserRepository
from models.users_model import User
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersService:
    def __init__(self, db_session):
        self.users_repository = UserRepository(db_session)

    def authenticate_user(self, email: str, password: str):
        user = self.users_repository.db.query(User).filter(User.email == email).first()
        logger.info(f"Authenticating user: {email}")
        if user and check_password_hash(user.password, password):
            logger.info(f"User authenticated successfully: {email}")
            return user
        logger.warning(f"Failed authentication attempt: {email}")
        return None

    def get_all_users(self):
        logger.info("Fetching all users")
        return self.users_repository.get_all_users()

    def get_user_by_id(self, user_id: int):
        logger.info(f"Fetching user by ID: {user_id}")
        return self.users_repository.get_user_by_id(user_id)

    def create_user(self, email: str, password: str,role:str="admin"):
        password_hashed = generate_password_hash(password)
        logger.info(f"Creating user: {email}")
        return self.users_repository.create_user(email, password_hashed,role)
    

    def update_user(self, user_id: int, email: str = None, password: str = None, role: str = None):
        logger.info(f"Updating user: {user_id}")
        return self.users_repository.update_user(user_id, email, password, role)

    def delete_user(self, user_id: int):
        logger.info(f"Deleting user: {user_id}")
        return self.users_repository.delete_user(user_id)