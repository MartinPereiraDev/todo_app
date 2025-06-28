from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.infrastructure.database import get_session
from app.models.task import Task
from app.models.user import User
from app.models.task_list import TaskList
from app.domain.schemas.task import TaskResponse, TaskUpdate
from app.domain.schemas.user import UserResponse
from app.domain.schemas.task_list import TaskListCreate, TaskListResponse
from typing import Optional, List
from sqlalchemy.exc import IntegrityError

router = APIRouter()


# create task
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: Task,
    session: Session = Depends(get_session)
):
    try:
        # check if user exists
        user = session.get(User, task_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # check if task list exists if provided
        if task_data.list_id:
            task_list = session.get(TaskList, task_data.list_id)
            if not task_list:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task list with ID {task_data.list_id} not found"
                )

        # create task
        task = Task(**task_data.dict())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# get all tasks with filters
@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    session: Session = Depends(get_session),
    user_id:        Optional[int] = None,
    list_id:        Optional[int] = None,
    status:         Optional[str] = None,
    priority:       Optional[str] = None,
    min_progress:   Optional[int] = None,
    max_progress:   Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get all tasks
    
    Args:
        session: Database session
        user_id: Optional user ID to filter tasks by
        list_id: Optional list ID to filter tasks by
        status: Optional status to filter tasks by
        priority: Optional priority to filter tasks by
        min_progress: Optional minimum progress to filter tasks by
        max_progress: Optional maximum progress to filter tasks by
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
    
    Returns:
        List[TaskResponse]: List of tasks
    """
    try:
        statement = select(Task).options(joinedload(Task.user))
        
        # Apply filters
        if user_id:
            statement = statement.where(Task.user_id == user_id)
        if list_id:
            statement = statement.where(Task.list_id == list_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if min_progress is not None:
            statement = statement.where(Task.progress >= min_progress)
        if max_progress is not None:
            statement = statement.where(Task.progress <= max_progress)
        
        statement = statement.offset(skip).limit(limit)
        tasks = session.execute(statement).scalars().all()
        
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tasks: {str(e)}"
        )

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    Get a specific task
    
    Args:
        task_id: ID of the task to retrieve
    
    Returns:
        TaskResponse: The retrieved task
    
    Raises:
        HTTPException: If task is not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

# update task
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: Task,
    session: Session = Depends(get_session)
):
    """
    Update a specific task
    
    Args:
        task_id: ID of the task to update
        task_data: Data to update the task
    
    Raises:
        HTTPException: If task is not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Update task status and priority
@router.put("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update the status and/or priority of a task
    
    Args:
        task_id: ID of the task to update
        task_update: Data containing status and/or priority to update
    
    Returns:
        TaskResponse: The updated task
    
    Raises:
        HTTPException: If task is not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not exists"
        )

    # Update only the fields that were provided
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.progress is not None:
        task.progress = task_update.progress

    # Update updated_at timestamp
    task.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(task)
    return task

# Delete a specific task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not exists"
        )

    try:
        session.delete(task)
        session.commit()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
