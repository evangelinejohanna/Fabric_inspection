import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np

# Define class labels (extracted from your classification report)
class_names = ["Vertical", "Defect Free", "Horizontal", "Hole", "Lines", "Stain"]

# Load the trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize ResNet18 model with same structure as trained model
model = models.resnet18(weights=False)  
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(class_names))  # Adjust output layer to match class count

# Load saved model weights
model.load_state_dict(torch.load('C:\\Users\\Evangeline Johanna\\OneDrive\\Documents\\FABRIC_INSP\\backend\\model\\fabric_defect_model.pth', map_location=device))
model.to(device)
model.eval()  # Set model to evaluation mode

# Image preprocessing function
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    try:
        image = Image.open(image_path).convert('RGB')  # Ensure image is in RGB format
        image = transform(image).unsqueeze(0)  # Add batch dimension
        return image.to(device)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Prediction function
def predict_image(image_path):
    image = preprocess_image(image_path)  
    if image is None:
        return "Error: Invalid image", None

    with torch.no_grad():  # No gradients needed
        outputs = model(image)  # Forward pass
        probabilities = torch.softmax(outputs, dim=1)  # Convert to probabilities
        predicted_class = torch.argmax(probabilities, dim=1).item()  # Get highest probability class

    return class_names[predicted_class], probabilities.cpu().numpy()

# Test with a new image
image_path = "C:\\Users\\Evangeline Johanna\\OneDrive\\Documents\\FABRIC_INSP\\Fabric Defect Dataset\\defected\\Vertical\\2.jpg"  # Path to your captured image
predicted_label, probabilities = predict_image(image_path)

# Print result
print(f"Predicted Defect Type: {predicted_label}")
print(f"Class Probabilities: {probabilities}")
