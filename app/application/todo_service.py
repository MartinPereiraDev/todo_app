from sqlmodel import select, func
from app.domain import todo_models
from app.models import TodoListDB, TaskDB
from app.infrastructure.database import get_session
from app.core.errors import NotFoundError

class TodoService:
    """Service handling todo list operations"""
    
    def __init__(self, session):
        self.session = session
    
    def create_todo_list(self, list_data: todo_models.TodoListCreate) -> TodoListDB:
        """
        Create a new todo list
        
        Args:
            list_data: Data for the new todo list
            
        Returns:
            Newly created todo list object
        """
        db_list = TodoListDB(**list_data.dict())
        self.session.add(db_list)
        self.session.commit()
        self.session.refresh(db_list)
        return db_list

    # Other CRUD methods with similar documentation

class TaskService:
    """Service handling task operations"""
    
    def __init__(self, session):
        self.session = session
    
    def get_tasks_with_completion(
        self, 
        list_id: int, 
        status: todo_models.Status = None, 
        priority: todo_models.Priority = None
    ) -> list[todo_models.TaskResponse]:
        """
        Get tasks with completion percentage
        
        Args:
            list_id: ID of parent todo list
            status: Optional status filter
            priority: Optional priority filter
            
        Returns:
            List of tasks with completion percentage
        """
        # Base query
        query = select(TaskDB).where(TaskDB.todo_list_id == list_id)
        
        # Apply filters
        if status:
            query = query.where(TaskDB.status == status)
        if priority:
            query = query.where(TaskDB.priority == priority)
        
        # Execute query
        tasks = self.session.exec(query).all()
        
        # Calculate completion percentage if filtered
        if status or priority:
            total_tasks = self.session.exec(
                select(func.count()).where(TaskDB.todo_list_id == list_id)
            ).one()
            completion = (len(tasks) / total_tasks * 100) if total_tasks else 0
        else:
            completion = None
        
        # Format response
        return [
            todo_models.TaskResponse(
                **task.dict(),
                completion_percentage=completion
            )
            for task in tasks
        ]

    # Other task methods