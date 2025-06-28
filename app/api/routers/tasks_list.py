from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.infrastructure.database import get_session
from app.models.task_list import TaskList
from app.models.user import User
from app.domain.schemas.task_list import TaskListCreate, TaskListResponse
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

router = APIRouter()

# Create a new task list
@router.post("/", response_model=TaskListResponse, status_code=status.HTTP_201_CREATED)
def create_task_list(
    task_list_data: TaskListCreate,
    session: Session = Depends(get_session)
):
    try:
        # Check if user exists
        user = session.get(User, task_list_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create task list
        task_list = TaskList(**task_list_data.dict())
        session.add(task_list)
        session.commit()
        session.refresh(task_list)
        return task_list

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Get all task lists for a user
@router.get("/", response_model=List[TaskListResponse])
def get_task_lists(
    user_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(TaskList)
    
    if user_id:
        query = query.where(TaskList.user_id == user_id)
    
    task_lists = session.execute(query).scalars().all()
    return task_lists

# Get a specific task list
@router.get("/{task_list_id}", response_model=TaskListResponse)
def get_task_list(
    task_list_id: int,
    session: Session = Depends(get_session)
):
    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    return task_list

# Update a task list
@router.put("/{task_list_id}", response_model=TaskListResponse)
def update_task_list(
    task_list_id: int,
    task_list_data: TaskListCreate,
    session: Session = Depends(get_session)
):
    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found or not exists"
        )

    try:
        # Check if user exists
        user = session.get(User, task_list_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or not exists"
            )

        # Update task list
        for key, value in task_list_data.dict().items():
            setattr(task_list, key, value)
        
        session.commit()
        session.refresh(task_list)
        return task_list

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Delete a task list
@router.delete("/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_list(
    task_list_id: int,
    session: Session = Depends(get_session)
):
    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found or not exists"
        )

    session.delete(task_list)
    session.commit()
    return None