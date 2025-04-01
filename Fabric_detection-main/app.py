from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
import cv2
import torch
from io import BytesIO

app = FastAPI()

# Load AI model
model = torch.load("fabric_model_resnet50.pth", map_location=torch.device("cpu"))
model.eval()

def process_image(image):
    img_array = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))  # Adjust size if needed
    img_tensor = torch.tensor(img).unsqueeze(0).float()
    return img_tensor

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    img_tensor = process_image(await file.read())
    result = model(img_tensor)  # Run AI Model
    return {"defect": result.tolist()}  # Return prediction

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
