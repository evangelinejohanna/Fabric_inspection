import torch
import cv2
import os
import time
from torchvision import transforms, models
from torchvision.models import ResNet50_Weights
from PIL import Image
import json

# Load the trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
model.fc = torch.nn.Linear(model.fc.in_features, 5)  # Adjust to your number of classes
model.load_state_dict(torch.load("model.pth", map_location=device))
model.to(device)
model.eval()

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Class names (adjust according to your dataset)
class_names = ["defect_free", "hole", "horizontal", "lines", "vertical"]

# Create a directory to save images
save_dir = 'captured_images'
os.makedirs(save_dir, exist_ok=True)

# Start capturing video from the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

print("Automatic image capture started. Press 'q' to quit.")

# Set the interval for automatic capture (in seconds)
capture_interval = 5  # Capture every 5 seconds
last_capture_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    current_time = time.time()
    if current_time - last_capture_time >= capture_interval:
        # Convert the frame to PIL Image for processing
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Preprocess the image
        image_tensor = transform(image).unsqueeze(0).to(device)

        # Make prediction
        with torch.no_grad():
            output = model(image_tensor)
            predicted_class = torch.argmax(output).item()

        # Get the label for the predicted class
        label = class_names[predicted_class]

        # Save the captured image with the defect label
        image_filename = os.path.join(save_dir, f'image_{predicted_class}.jpg')
        def save_defect_results(image_path, defect_type):
         """Save defect detection results in a JSON file."""
         result_data = {
                "image_path": image_path,
                "defect_type": defect_type         
            }
         with open("defect_results.json", "w") as file:
            json.dump(result_data, file)

        try:
            # Overlay the label on the frame
            cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # Save the captured image
            cv2.imwrite(image_filename, frame)  
            print(f"Image saved as {image_filename} with label: {label}")
            save_defect_results(image_filename, label)
            last_capture_time = current_time  # Update the last capture time
        except Exception as e:
            print(f"Error saving image: {e}")

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()