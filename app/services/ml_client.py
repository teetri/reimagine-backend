from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
from app.services import storage
from PIL import Image

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def choose_size(image_path):
    img = Image.open(image_path)
    w, h = img.size

    ratio = w / h

    if ratio > 1.2:
        return "1536x1024"   # landscape
    elif ratio < 0.8:
        return "1024x1536"   # portrait
    else:
        return "1024x1024"   # square


def generate_image(prompt, image_path):

    size = choose_size(image_path)

    response = client.images.edit(
        model="gpt-image-1",
        image=open(image_path, "rb"),
        prompt=prompt,
        size=size
    )

    image_base64 = response.data[0].b64_json

    saved_path = storage.save_generated_image(image_base64)

    return saved_path
