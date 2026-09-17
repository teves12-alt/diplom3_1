import logging
import pytest
from selenium import webdriver

from helpers import generate_user_data, register_user, login_user, delete_user
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage

# Создаём логгер
logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def order_feed_page(driver):
    return OrderFeedPage(driver)


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def auth_user(driver, user_data):
    # 1. Попытка регистрации
    reg_response = register_user(user_data)
    
    # Если регистрация вернула ошибку "user already exists", игнорируем и идём дальше
    if reg_response.status_code == 403: 
        # Пользователь уже есть, ничего не делаем, пробуем залогиниться
        pass
    elif reg_response.status_code != 200:
        raise Exception(f"Не удалось зарегистрировать пользователя: {reg_response.text}")

    # 2. Логинимся
    login_response = login_user({
        "email": user_data["email"],
        "password": user_data["password"],
    })

    assert login_response.status_code == 200, f"Логин не удался: {login_response.text}"
    
    data = login_response.json()
    assert "accessToken" in data, f"В ответе нет accessToken: {data}"
    
    token = data["accessToken"]
    user_data["token"] = token

    yield user_data

    # 3. Удаляем пользователя (обязательно!)
    try:
        delete_user({"Authorization": token})
    except Exception as e:
        logger.error(f"Не удалось удалить пользователя после теста: {e}")

