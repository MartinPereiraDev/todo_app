import pytest
from sqlmodel import Session
from app.models import User
from app.domain.schemas.user import UserUpdate

@pytest.mark.integration
class TestUserIntegration:
    def test_update_user(self, client, session: Session, test_data):
        """Test for updating a user"""
        # Get the user created in the test_data fixture
        user = test_data["user"]
        
        # Update data
        update_data = {
            "name": "Nombre Actualizado",
            "surname": "Apellido Actualizado",
            "email": "nuevo_email@example.com"
        }
        
        # Perform the PUT request to update the user
        response = client.put(
            f"/api/v1/users/{user.id}",
            json=update_data
        )
        
        # Verify response
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "Nombre Actualizado"
        assert updated_user["surname"] == "Apellido Actualizado"
        assert updated_user["email"] == "nuevo_email@example.com"
        
        # Verify in the database
        db_user = session.get(User, user.id)
        assert db_user.name == "Nombre Actualizado"
        assert db_user.surname == "Apellido Actualizado"
        assert db_user.email == "nuevo_email@example.com"

    def test_update_user_partial(self, client, session: Session, test_data):
        """Test for updating a user partially"""
        user = test_data["user"]
        
        # Update only the name
        response = client.put(
            f"/api/v1/users/{user.id}",
            json={"name": "Solo Nombre Actualizado"}
        )
        
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "Solo Nombre Actualizado"
        
        # Verify that other fields did not change
        db_user = session.get(User, user.id)
        assert db_user.surname == test_data["user"].surname
        assert db_user.email == test_data["user"].email

    def test_update_user_invalid(self, client, test_data):
        """Test for invalid update"""
        user = test_data["user"]
        
        # Try to update with invalid email
        response = client.put(
            f"/api/v1/users/{user.id}",
            json={"email": "email-invalido"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity

    def test_update_nonexistent_user(self, client):
        """Test for updating a non-existent user"""
        response = client.put(
            "/api/v1/users/9999",
            json={"name": "Inexistente"}
        )
        assert response.status_code == 404