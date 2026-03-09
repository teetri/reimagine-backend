import base64
import os
import uuid

UPLOAD_DIR = "app/temp/uploads"


def save_upload(file):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path


OUTPUT_DIR = "app/temp/outputs"


def save_generated_image(image_base64):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "wb") as f:
        f.write(base64.b64decode(image_base64))

    return path
