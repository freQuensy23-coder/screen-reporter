from PIL import Image
import httpx
from loguru import logger
import base64
import io
import json

def get_user_activity_description(image: Image.Image, user_id: int, secret_key: str) -> str:
    # Конвертируем изображение в base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    with httpx.Client() as client:
        try:
            response = client.post(
                "http://localhost:8000/screenshot",
                json={
                    "user_id": user_id,
                    "image_base64": img_str,
                    "user_secret_key": secret_key,
                },
                timeout=30.0,
            )
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response content: {response.text}")

            response.raise_for_status()
            
            try:
                return response.json()["result"]
            except (KeyError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse response JSON: {e}")
                logger.error(f"Response content: {response.text}")
                raise ValueError(f"Invalid response from server: {e}")
                
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise
