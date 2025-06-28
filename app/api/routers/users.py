from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.infrastructure.database import get_session
from app.models.user import User


router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: User,
    session: Session = Depends(get_session)
):
    try:
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# enpoint lists all users
@router.get("/", response_model=list[User])
def get_all_users(session: Session = Depends(get_session)):
    # get all users
    statement = select(User)
    users = session.exec(statement).all()
    return users
