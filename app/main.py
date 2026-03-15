import os

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import json

from fastapi.staticfiles import StaticFiles
from app.services import storage, image_processor, ml_client, prompt_builder

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="app/temp/outputs"), name="outputs")


@app.post("/generate")
async def generate_design(
    room_image: UploadFile = File(...),
    inspiration_image: UploadFile | None = File(None),
    text_input: str = Form(...)
):

    # Validate room image
    if not room_image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Room image must be an image")

    # Save + preprocess room image
    room_image_path = storage.save_upload(room_image)
    room_image_path = image_processor.preprocess_image(room_image_path)

    inspiration_image_path = None

    # Handle optional inspiration image
    if inspiration_image:
        if not inspiration_image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="Inspiration image must be an image")

        inspiration_image_path = storage.save_upload(inspiration_image)
        inspiration_image_path = image_processor.preprocess_image(
            inspiration_image_path)

    # Parse JSON text input
    try:
        data = json.loads(text_input)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON in text_input")

    # Build prompt (tell prompt builder if inspiration exists)
    prompt = prompt_builder.build_prompt(
        data,
        has_inspiration=inspiration_image_path is not None
    )

    # Generate image
    # try:
    generated_image_path = ml_client.generate_image(
        prompt,
        room_image_path,
        inspiration_image_path
    )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Image generation failed")

    return {
        "generated_image_url": f"/outputs/{os.path.basename(generated_image_path)}"
    }
