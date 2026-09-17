import uuid
import requests

from data import BASE_URL


def generate_user_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "password": "123456",
        "name": f"User_{unique_id}"
    }


def register_user(user_data):
    url = f"{BASE_URL}/api/auth/register"
    response = requests.post(url, json=user_data)
    return response


def login_user(credentials):
    url = f"{BASE_URL}/api/auth/login"
    response = requests.post(url, json=credentials)
    return response


def delete_user(headers):
    url = f"{BASE_URL}/api/auth/user"
    response = requests.delete(url, headers=headers)
    return response

