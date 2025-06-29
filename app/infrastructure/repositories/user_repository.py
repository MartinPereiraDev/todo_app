from sqlmodel import select, Session
from app.models.user import User
from app.domain.exceptions import NotFoundError

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        user = self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        user = self.session.execute(statement).scalars().first()
        if not user:
            raise NotFoundError("User not found")
        return user

    def update(self, user_id: int, user_data: dict) -> User:
        user = self.get_by_id(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.session.delete(user)
        self.session.commit()

    
    