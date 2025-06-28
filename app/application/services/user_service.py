from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.schemas.user import UserCreate, UserResponse
from app.models.user import User
from passlib.context import CryptContext
from app.domain.exceptions import NotFoundError, BadRequestError 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> UserResponse:
        try:
            # Check if email already exists
            self.repository.get_by_email(user_data.email)
            raise BadRequestError("Email already registered")
        except NotFoundError:
            # Email not found, proceed with user creation
            # Hash password
            hashed_password = pwd_context.hash(user_data.password)
            
            # Create user
            db_user = User(
                name        = user_data.name,
                surname     = user_data.surname,
                email       = user_data.email,
                password    = hashed_password,
                role        = user_data.role
            )
            
            return self.repository.create(db_user)

    def get_user(self, user_id: int) -> User:
        return self.repository.get_by_id(user_id)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        if not pwd_context.verify(password, user.password):
            raise ValueError("Invalid credentials")
        return user

