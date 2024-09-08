import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestAccounts:
    
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user_data(self):
        return {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123!",
            "password2": "Testpassword123!"
        }

    @pytest.fixture
    def create_user(self, user_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password1"]
        )
        return user

    def test_register_user(self, client, user_data):
        url = reverse("register")
        response = client.post(url, user_data, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_signin(self, client, create_user, user_data):
        url = reverse("signin")
        login_data = {
            "username": user_data["username"],
            "password": user_data["password1"]
        }
        response = client.post(url, login_data, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_get_user_detail(self, client, create_user):
        url = reverse("user-detail", kwargs={"username": create_user.username})
        client.force_authenticate(user=create_user)
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == create_user.username
        assert response.data["email"] == create_user.email

    def test_update_user_detail(self, client, create_user):
        url = reverse("user-detail", kwargs={"username": create_user.username})
        updated_data = {"username": "updateduser"}
        client.force_authenticate(user=create_user)
        response = client.put(url, updated_data, format="json")
        assert response.status_code == 200
        assert response.data["username"] == "updateduser"

    def test_change_password(self, client, create_user):
        url = reverse("change-password")
        change_password_data = {
            "old_password": "Testpassword123!",
            "new_password1": "NewPassword123!",
            "new_password2": "NewPassword123!"
        }
        client.force_authenticate(user=create_user)
        response = client.put(url, change_password_data, format="json")
        assert response.status_code == 200
        assert response.data["detail"] == "Password has been changed successfully."

    def test_delete_user(self, client, create_user):
        url = reverse("register")
        client.force_authenticate(user=create_user)
        response = client.delete(url, {"password": "Testpassword123!"}, format="json")
        assert response.status_code == 204
        assert get_user_model().objects.filter(username=create_user.username).count() == 0
