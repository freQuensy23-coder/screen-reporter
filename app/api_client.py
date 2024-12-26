from PIL import Image
import httpx

def get_user_activity_description(image: Image.Image) -> str:
    with httpx.Client() as client:
        response = client.post(
            "http://localhost:8000/screenshot",
            json={"image": image.tobytes()},
        )
        return response.json()["result"]
