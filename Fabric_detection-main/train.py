import torch
import os
from torchvision import datasets, transforms, models

# Set dataset path
#dataset_path = "/home/student/tnwise/Fabric_Defect_Dataset"
dataset_path = "C:\\Users\\Evangeline Johanna\\OneDrive\\Documents\\FABRIC_INSP\\Fabric Defect Dataset"

# Define image transformations
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load dataset
dataset = datasets.ImageFolder(root=dataset_path, transform=train_transform)
train_loader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)

# Define model (ResNet50 for example)
model = models.resnet50(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, len(dataset.classes))

# Train the model (Basic Training Loop)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

print("Training Started...")
for epoch in range(5):  # Train for 5 epochs
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1} done!")

# Save model
torch.save(model.state_dict(), "model.pth")
print("Model saved as fabric_model.pth")


