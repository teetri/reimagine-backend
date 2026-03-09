import os

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import json

from fastapi.staticfiles import StaticFiles
from app.services import storage, image_processor, ml_client, prompt_builder

app = FastAPI()


@app.post("/generate")
async def generate_design(
    room_image: UploadFile = File(...),
    text_input: str = Form(...)
):
    if not room_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    room_image_path = storage.save_upload(room_image)
    room_image_path = image_processor.preprocess_image(room_image_path)

    from fastapi import HTTPException

    try:
        data = json.loads(text_input)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON in text_input")

    prompt = prompt_builder.build_prompt(data)

    try:
        generated_image_path = ml_client.generate_image(
            prompt, room_image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Image generation failed")

    app.mount("/outputs", StaticFiles(directory="app/temp/outputs"),
              name="outputs")

    return {
        "generated_image_url": f"/outputs/{os.path.basename(generated_image_path)}"
    }
