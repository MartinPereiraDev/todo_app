from app.infrastructure.repositories.task_repository import TaskRepository
from app.domain.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.domain.exceptions import NotFoundError

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        return self.repository.create(task_data)

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID"""
        task = self.repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task

    def update_task(self, task_id: int, update_data: TaskUpdate) -> Task:
        """Update an existing task"""
        existing_task = self.repository.get_by_id(task_id)
        if not existing_task:
            raise NotFoundError("Task not found")
        
        # Update fields
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(existing_task, key, value)
        
        return self.repository.update(task_id, existing_task)

    def delete_task(self, task_id: int) -> None:
        """Delete a task"""
        task = self.repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        self.repository.delete(task_id)
