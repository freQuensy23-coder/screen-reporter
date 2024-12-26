import os
import sys
from datetime import datetime
from app.api_client import get_user_activity_description
from screenshot import make_screenshot
from server.utils import tqdm_sleep
import time
from loguru import logger
import signal
import atexit
import requests
from config import get_credentials, save_credentials

MINUTE = 60
SERVER_URL = "http://localhost:8000"  # Измените на реальный URL сервера


def register_user() -> tuple[int, str]:
    response = requests.post(f"{SERVER_URL}/register")
    if response.status_code != 200:
        raise Exception("Failed to register user")
    
    data = response.json()
    return data["user_id"], data["secret_key"]

def login(user_id: int, secret_key: str) -> bool:
    response = requests.post(
        f"{SERVER_URL}/login",
        params={"user_id": user_id, "secret_key": secret_key}
    )
    return response.status_code == 200

def run_daemon():
    logger.info("Activity tracker daemon started")
    
    # Получаем или создаем учетные данные
    user_id, secret_key = get_credentials()
    if user_id is None or secret_key is None:
        logger.info("No credentials found. Registering new user...")
        user_id, secret_key = register_user()
        save_credentials(user_id, secret_key)
        logger.info(f"Registered new user with ID: {user_id}")
    
    # Проверяем валидность учетных данных
    if not login(user_id, secret_key):
        logger.error("Invalid credentials. Please reinstall the application.")
        user_id, secret_key = register_user()
        save_credentials(user_id, secret_key)
        return
    
    logger.info("Successfully logged in")
    
    while True:
        try:
            screenshot = make_screenshot()
            activity_description = get_user_activity_description(screenshot)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{timestamp}] {activity_description}")
            time.sleep(3 * MINUTE)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            time.sleep(MINUTE)

if __name__ == "__main__":
    run_daemon() 