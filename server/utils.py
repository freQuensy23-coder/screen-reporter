import tqdm
import time
from PIL import Image
import io
import base64
from functools import lru_cache


@lru_cache(maxsize=8)
def read_file_cached(file_name: str) -> str:
    with open(file_name, "r") as f:
        return f.read()


def tqdm_sleep(seconds: int) -> None:
    for _ in tqdm.tqdm(range(seconds), desc="Sleeping"):
        time.sleep(1)


def encode_image(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return (
        f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    )
