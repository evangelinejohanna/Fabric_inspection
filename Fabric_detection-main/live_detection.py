import cv2
import os

# Create a directory to save images
save_dir = 'captured_images'
os.makedirs(save_dir, exist_ok=True)

# Start capturing video from the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

print("Press 'c' to capture an image and 'q' to quit.")

image_count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  # Press 'c' to capture an image
        image_filename = os.path.join(save_dir, f'image_{image_count}.jpg')
        cv2.imwrite(image_filename, frame)  # Save the captured image
        print(f"Image saved as {image_filename}")
        image_count += 1
    elif key == ord('q'):  # Press 'q' to quit
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()