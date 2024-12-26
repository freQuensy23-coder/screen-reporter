import tempfile
import os
import time
from PIL import Image


def make_screenshot() -> Image.Image:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        file_name = tmp_file.name
    os.system(f"screencapture {file_name}")

    image = Image.open(file_name)

    os.remove(file_name)

    return image
