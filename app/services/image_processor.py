from PIL import Image
import os


def preprocess_image(path, max_size=1024):
    img = Image.open(path)

    img.thumbnail((max_size, max_size))

    img = img.convert("RGB")

    new_path = os.path.splitext(path)[0] + ".png"

    img.save(new_path, format="PNG", optimize=True)

    return new_path
