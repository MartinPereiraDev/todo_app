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
    """
    Create a new task list
    
    Args:
        task_list_data: Data to create the task list
    
    Returns:
        TaskListResponse: The created task list
    
    Raises:
        HTTPException: If user is not found or not exists
    """
    try:
        # Check if user exists
        user = session.get(User, task_list_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or not exists"
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
    """
    Get all task lists for a user
    
    Args:
        user_id: Optional user ID to filter task lists by
    
    Returns:
        List[TaskListResponse]: List of task lists
    """
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
    """
    Get a specific task list
    
    Args:
        task_list_id: ID of the task list
    
    Returns:
        TaskListResponse: The retrieved task list
    
    Raises:
        HTTPException: If task list is not found or not exists
    """
    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found or not exists"
        )
    return task_list

# Update a task list
@router.put("/{task_list_id}", response_model=TaskListResponse)
def update_task_list(
    task_list_id: int,
    task_list_data: TaskListCreate,
    session: Session = Depends(get_session)
):
    """
    Update a task list
    
    Args:
        task_list_id: ID of the task list
        task_list_data: Data to update the task list
    
    Raises:
        HTTPException: If task list is not found
    """
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

# Delete all tasks from a task list
@router.delete("/{task_list_id}/tasks", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_tasks_from_list(
    task_list_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete all tasks associated with a specific task list
    
    Args:
        task_list_id: ID of the task list
    
    Raises:
        HTTPException: If task list is not found
    """
    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )

    # Delete all tasks associated with this list
    session.query(Task).filter(Task.list_id == task_list_id).delete()
    session.commit()
    return None

# Delete a task list
@router.delete("/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_list(
    task_list_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a task list
    
    Args:
        task_list_id: ID of the task list
    
    Raises:
        HTTPException: If task list is not found
    """

    task_list = session.get(TaskList, task_list_id)
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found or not exists"
        )

    session.delete(task_list)
    session.commit()
    return None