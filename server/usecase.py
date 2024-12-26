from .utils import encode_image
from models import User, ImageProcessingResult, peewee
import uuid
from loguru import logger
from typing import Optional, Tuple
from PIL import Image
import openai
from utils import read_file_cached
from dotenv import load_dotenv
from async_lru import alru_cache
import io

load_dotenv()

client = openai.AsyncClient()


def register_user() -> Tuple[Optional[User], Optional[str]]:
    try:
        secret_key = uuid.uuid4().hex
        user = User.create(secret_key=secret_key, is_active=True)
        logger.info(f"Created new user with ID: {user.id}")
        return user, None
    except peewee.IntegrityError as e:
        error_msg = "Failed to create user due to database constraint"
        logger.error(f"{error_msg}: {str(e)}")
        return None, error_msg
    except Exception as e:
        error_msg = "Unexpected error during user registration"
        logger.error(f"{error_msg}: {str(e)}")
        return None, error_msg


def login(user_id: int, user_key: str) -> Tuple[bool, Optional[str]]:
    try:
        user = User.get_or_none(
            (User.secret_key == user_key)
            & (User.id == user_id)
            & (User.is_active == True)
        )
        if user is None:
            return False, "Invalid credentials or user is inactive"
        logger.info(f"Successful login for user ID: {user_id}")
        return True, None
    except Exception as e:
        error_msg = "Error during login"
        logger.error(f"{error_msg}: {str(e)}")
        return False, error_msg


@alru_cache(maxsize=256)
async def process_image(image: Image) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": read_file_cached("prompt.md"),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "User activity screenshot"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encode_image(image=image),
                        },
                    },
                ],
            },
        ],
    )
    if response.choices[0].message.content is None:
        raise ValueError("No response from LLM")
    return response.choices[0].message.content


def get_history(
    user_id: int, start_date: str, end_date: str
) -> list[ImageProcessingResult]:
    history = (
        ImageProcessingResult.select()
        .where(
            (ImageProcessingResult.user == user_id)
            & (ImageProcessingResult.created_at >= start_date)
            & (ImageProcessingResult.created_at <= end_date)
        )
        .order_by(ImageProcessingResult.created_at.desc())
    )
    return history
