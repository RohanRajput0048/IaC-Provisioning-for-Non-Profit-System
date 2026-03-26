import bcrypt
import logging
from src.services.db_service import db_service

logger = logging.getLogger(__name__)

class UserService:
    def create_user(self, email: str, password: str) -> bool:
        """Create a new user with a hashed password. Returns True if successful, False if email exists."""
        db_service._init_db()
        collection = db_service.db.get_collection("users")
        
        # Check if user already exists
        existing_user = collection.find_one({"email": email})
        if existing_user:
            return False
            
        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        
        user_doc = {
            "email": email,
            "password_hash": hashed
        }
        
        try:
            collection.insert_one(user_doc)
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False

    def verify_user(self, email: str, password: str) -> bool:
        """Verify user credentials. Returns True if valid, False otherwise."""
        db_service._init_db()
        collection = db_service.db.get_collection("users")
        
        user = collection.find_one({"email": email})
        if not user:
            return False
            
        # Check password
        return bcrypt.checkpw(password.encode("utf-8"), user["password_hash"])

    def reset_password(self, email: str, new_password: str) -> bool:
        """Reset user password. Returns True if successful, False if user not found."""
        db_service._init_db()
        collection = db_service.db.get_collection("users")
        
        user = collection.find_one({"email": email})
        if not user:
            return False
            
        # Hash new password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), salt)
        
        try:
            collection.update_one(
                {"email": email},
                {"$set": {"password_hash": hashed}}
            )
            return True
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            return False

user_service = UserService()
