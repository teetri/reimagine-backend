from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
from app.services import storage
from PIL import Image

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


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


def generate_image(prompt, room_image_path, inspiration_image_path=None):

    size = choose_size(room_image_path)

    room_base64 = encode_image(room_image_path)

    content = [
        {"type": "input_text", "text": prompt},
        {
            "type": "input_image",
            "image_url": f"data:image/png;base64,{room_base64}"
        }
    ]

    # Add inspiration image if provided
    if inspiration_image_path:
        inspo_base64 = encode_image(inspiration_image_path)

        content.append({
            "type": "input_image",
            "image_url": f"data:image/png;base64,{inspo_base64}"
        })

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": content
            }
        ],
        tools=[{
            "type": "image_generation",
            "size": size
        }]
    )

    # Extract generated image from response
    image_generation_calls = [
        output for output in response.output
        if output.type == "image_generation_call"
    ]

    image_base64 = image_generation_calls[0].result

    saved_path = storage.save_generated_image(image_base64)

    return saved_path
