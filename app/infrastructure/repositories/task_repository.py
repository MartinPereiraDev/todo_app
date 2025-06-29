from sqlmodel import select, Session
from app.models.task import Task
from app.domain.exceptions import NotFoundError

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: Task) -> Task:
        """Create a new task"""
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task:
        """Get a task by ID"""
        task = self.session.get(Task, task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task

    def update(self, task_id: int, task_data: Task) -> Task:
        """Update an existing task"""
        task = self.get_by_id(task_id)
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        """Delete a task"""
        task = self.get_by_id(task_id)
        self.session.delete(task)
        self.session.commit()
