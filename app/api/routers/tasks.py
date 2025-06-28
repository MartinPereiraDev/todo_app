from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.infrastructure.database import get_session
from app.models.task import Task, TaskCreate
from app.models.user import User
from app.domain.schemas.task import TaskResponse
from app.domain.schemas.user import UserResponse
from typing import Optional
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
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
            
        task = Task(
            user_id=task_data.user_id,
            task=task_data.task,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            progress=task_data.progress

        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
"""
# enpoint lists all tasks
@router.get("/", response_model=list[Task])
def get_all_tasks(session: Session = Depends(get_session)):
    # get all tasks
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks
    """
     
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    session: Session = Depends(get_session),
    user_id: Optional[int] = None
):
    statement = select(Task).options(joinedload(Task.user))
    
    if user_id:
        statement = statement.where(Task.user_id == user_id)
    
    tasks = session.exec(statement).all()
    
    # Convertir a esquema de respuesta que incluye usuario
    return [
        TaskResponse(
            id=task.id,
             user= UserResponse(
                id=task.user.id,
                name=task.user.name,
                surname=task.user.surname,
                email=task.user.email,
                role=task.user.role
            ),
            type=task.type,
            task=task.task,
            priority=task.priority,
            status=task.status,
            progress=task.progress,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]