import torch
import torchvision.transforms as transforms
from PIL import Image
import os
from torchvision import models

# Load trained model
model = models.resnet50(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, 6)  # 5 classes
model.load_state_dict(torch.load("fabric_model_resnet50.pth", weights_only=False))

model.eval()

# Define transformations for input images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Ask user for image path
image_path = input("Enter the image file path: ")

if not os.path.exists(image_path):
    print("Error: File not found!")
else:
    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    # Predict
    with torch.no_grad():
        output = model(image)
        predicted_class = torch.argmax(output).item()

    class_names = ["defect_free", "hole", "horizontal", "lines", "stain", "vertical"]
    print(f"Prediction: {class_names[predicted_class]}")