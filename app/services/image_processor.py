from PIL import Image


def preprocess_image(path, max_size=1024):
    img = Image.open(path)

    img.thumbnail((max_size, max_size))

    img.save(path, optimize=True, quality=85)

    return path
