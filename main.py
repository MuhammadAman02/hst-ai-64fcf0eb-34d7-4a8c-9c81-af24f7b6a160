import os
from nicegui import ui, app
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from app.services.image_processing import process_image, change_skin_tone
from app.services.color_recommendation import get_color_recommendations

fastapi_app = FastAPI()
app.include_router(fastapi_app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@ui.page('/')
def home():
    ui.label('Skin Tone Color Recommendation App').classes('text-h3 mb-4')
    
    file = ui.upload(label='Upload Image', auto_upload=True).classes('mb-4')
    
    image = ui.image().classes('w-64 h-64 object-cover mb-4')
    recommendations = ui.label().classes('mb-4')
    
    skin_tone_slider = ui.slider(min=0, max=100, value=50, label='Adjust Skin Tone').classes('mb-4')
    
    async def handle_upload(e):
        if e.value:
            file_path = os.path.join(UPLOAD_DIR, e.name)
            with open(file_path, "wb") as f:
                f.write(e.content.read())
            
            processed_image_path = process_image(file_path)
            image.set_source(processed_image_path)
            
            colors = get_color_recommendations(processed_image_path)
            recommendations.set_text(f"Recommended colors: {', '.join(colors)}")
    
    async def update_skin_tone(e):
        if file.value:
            file_path = os.path.join(UPLOAD_DIR, file.value[0].name)
            adjusted_image_path = change_skin_tone(file_path, e.value)
            image.set_source(adjusted_image_path)
    
    file.on('upload', handle_upload)
    skin_tone_slider.on('change', update_skin_tone)

@fastapi_app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@fastapi_app.get("/image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(UPLOAD_DIR, image_name)
    return FileResponse(image_path)

if __name__ == "__main__":
    ui.run(port=8080, reload=False)