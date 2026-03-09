from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
from app.services import storage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_image(prompt, image_path):

    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-image-1",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    }
                ],
            }
        ],
        tools=[{"type": "image_generation"}],
    )

    image_generation_calls = [
        output for output in response.output
        if output.type == "image_generation_call"
    ]

    image_base64 = image_generation_calls[0].result

    saved_path = storage.save_generated_image(image_base64)

    return saved_path
