from PIL import Image
import time
import os


def make_screenshot() -> Image.Image:
    temp_dir = os.path.expanduser("~/Library/Application Support/ActivityTracker/temp")
    os.makedirs(temp_dir, exist_ok=True)
    file_name = os.path.join(temp_dir, f"screen_{time.time()}.png")
    os.system(f"screencapture {file_name}")
    image = Image.open(file_name)
    os.remove(file_name)  # Удаляем файл после загрузки в память
    return image
