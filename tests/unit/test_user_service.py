import pytest
from unittest.mock import MagicMock, patch
from app.application.services.user_service import UserService
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.schemas.user import UserUpdate, UserResponse
from app.models.user import User
from app.domain.exceptions import NotFoundError, BadRequestError
from datetime import datetime

@pytest.fixture
def mock_repository():
    """Fixture for a mock of UserRepository"""
    return MagicMock(spec=UserRepository)

@pytest.fixture
def user_service(mock_repository):
    """Fixture for the user service with mocked repository"""
    return UserService(mock_repository)

def test_update_user_success(user_service, mock_repository):
    """Test: Successful user update"""
    # 1. Configure test data
    user_id = 1
    existing_user = User(
        id=user_id,
        name="Original",
        surname="User",
        email="original@example.com",
        password="password",
        role="user"
    )
    
    update_data = UserUpdate(
        name="Actualizado",
        surname="Modificado",
        email="nuevo@example.com"
    )

    # 2. Configure mock behavior
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = None  # Email no existe
    mock_repository.update.return_value = User(
        id=existing_user.id,
        name="Actualizado",
        surname="Modificado",
        email="nuevo@example.com",
        password=existing_user.password,
        role=existing_user.role
    )

    # 3. Execute the method to test
    updated_user = user_service.update_user(user_id, update_data)

    # 4. Verify results
    assert updated_user.name == "Actualizado"
    assert updated_user.surname == "Modificado"
    assert updated_user.email == "nuevo@example.com"
    
    # 5. Verify interactions with the mock
    mock_repository.get_by_id.assert_called_once_with(user_id)
    mock_repository.update.assert_called_once()
    
    # check updated user
    updated_user_arg = mock_repository.update.call_args[0][0]
   

def test_update_user_partial(user_service, mock_repository):
    """Test: Partial user update"""
    # Configuration
    user_id = 1
    existing_user = User(
        id=user_id,
        name="Original",
        surname="User",
        email="original@example.com",
        password="password",
        role="user"
    )
    
    update_data = UserUpdate(name="Solo nombre actualizado")
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = None  # Email no existe
    mock_repository.update.return_value = User(
        id=existing_user.id,
        name="Solo nombre actualizado",
        surname=existing_user.surname,
        email=existing_user.email,
        password=existing_user.password,
        role="user"
    )

    # Execute
    updated_user = user_service.update_user(user_id, update_data)

    # Verify
    assert updated_user.name == "Solo nombre actualizado"
    assert updated_user.surname == "User"  # No cambió
    assert updated_user.email == "original@example.com"  # No cambió

def test_update_user_not_found(user_service, mock_repository):
    """Test: Attempt to update non-existent user"""
    # Configuration
    user_id = 999
    mock_repository.get_by_id.return_value = None
    
    # Execute and verify exception
    with pytest.raises(NotFoundError) as exc_info:
        user_service.update_user(user_id, UserUpdate(name="Nuevo nombre"))
    
    # Verify error message
    assert "User not found" in str(exc_info.value)
    mock_repository.get_by_id.assert_called_once_with(user_id)
    mock_repository.update.assert_not_called()

def test_update_user_email_conflict(user_service, mock_repository):
    """Test: Attempt to update to an existing email"""
    # Configuration
    user_id = 1
    existing_user = User(
        id=user_id,
        name="Usuario",
        surname="Existente",
        email="existente@example.com",
        password="password",
        role="user"
    )
    
    # Simular que ya existe un usuario con el nuevo email
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = User(id=2, email="nuevo@example.com")
    
    update_data = UserUpdate(email="nuevo@example.com")

    # Execute and verify exception
    with pytest.raises(BadRequestError) as exc_info:
        user_service.update_user(user_id, update_data)
    
    # Verify error message
    assert "Email already registered" in str(exc_info.value)
    mock_repository.get_by_email.assert_called_once_with("nuevo@example.com")
    mock_repository.update.assert_not_called()

def test_update_user_role_change(user_service, mock_repository):
    """Test: Role change for user"""
    # Configuration
    user_id = 1
    existing_user = User(
        id=user_id,
        name="Admin",
        surname="User",
        email="admin@example.com",
        password="password",
        role="admin"
    )
    
    update_data = UserUpdate(role="user")
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = None  # Email no existe
    mock_repository.update.return_value = User(
        id=existing_user.id,
        name="Solo nombre actualizado",
        surname=existing_user.surname,
        email=existing_user.email,
        password=existing_user.password,
        role="user"
    )

    updated_user = user_service.update_user(user_id, update_data)

    # check updated user
    assert updated_user.role == "user"
    updated_user_arg = mock_repository.update.call_args[0][0]
  