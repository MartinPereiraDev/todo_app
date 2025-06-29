from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.infrastructure.database import get_session
from app.models.user import User
from app.domain.schemas.user import UserResponse, UserCreate
from app.application.services.user_service import UserService
from app.infrastructure.repositories.user_repository import UserRepository
from typing import Optional, List
from sqlalchemy import select
from app.domain.exceptions import NotFoundError, BadRequestError 

router = APIRouter()

# CRUD Operations for Users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new user
    
    Args:
        user_data: User data to create
        session: Database session
    
    Returns:
        UserResponse: The created user
    
    Raises:
        HTTPException: If user already exists or other error occurs
    """
    try:
        # Create user service
        user_service = UserService(UserRepository(session))
        
        # Create user with hashed password
        user = user_service.create_user(user_data)
        return user
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    session: Session = Depends(get_session)
):
    """
    Get all users
    
    Args:
        session: Database session
    
    Returns:
        List[UserResponse]: List of all users
    """
    # get all users
    statement = select(User)
    users = session.execute(statement).scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Get a specific user
    
    Args:
        user_id: ID of the user to retrieve
        session: Database session
    
    Returns:
        UserResponse: The retrieved user
    
    Raises:
        HTTPException: If user is not found
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: User,
    session: Session = Depends(get_session)
):
    """
    Update a specific user
    
    Args:
        user_id: ID of the user to update
        user_data: Data to update the user
        session: Database session
    
    Returns:
        UserResponse: The updated user
    
    Raises:
        HTTPException: If user is not found
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user fields
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a specific user
    
    Args:
        user_id: ID of the user to delete
        session: Database session
    
    Raises:
        HTTPException: If user is not found
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        session.delete(user)
        session.commit()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
