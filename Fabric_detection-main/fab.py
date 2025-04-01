import cv2
import numpy as np
from sklearn.cluster import KMeans
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt

def open_image():
    """Open a file dialog to select an image."""
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Fabric Image",
                                           filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return file_path

def extract_dominant_colors(image_path, k=2):
    """Extract the top K dominant colors from the image."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_.astype(int)

    return [tuple(color) for color in colors], cv2.imread(image_path)

def rgb_to_lab(color):
    """Convert an RGB color to LAB color space."""
    color_array = np.uint8([[color]])
    lab_color = cv2.cvtColor(color_array, cv2.COLOR_RGB2LAB)[0][0]
    return lab_color

def lab_to_rgb(color):
    """Convert a LAB color to RGB color space."""
    color_array = np.uint8([[color]])
    rgb_color = cv2.cvtColor(color_array, cv2.COLOR_LAB2RGB)[0][0]
    return tuple(rgb_color)

def suggest_dyeing_solution(dominant_color, secondary_color):
    """Suggest a dye formula to shift secondary color toward the dominant color."""
    dominant_lab = rgb_to_lab(dominant_color)
    secondary_lab = rgb_to_lab(secondary_color)
    
    color_shift = dominant_lab - secondary_lab  # Compute shift in LAB space
    corrected_lab = secondary_lab + color_shift  # Apply correction
    corrected_lab = np.clip(corrected_lab, 0, 255)  # Ensure valid LAB values
    corrected_rgb = lab_to_rgb(corrected_lab)  # Convert back to RGB
    
    dye_formula = {
        "L Adjustment": color_shift[0],
        "A Adjustment": color_shift[1],
        "B Adjustment": color_shift[2]
    }
    
    return dye_formula, corrected_rgb

def process_fabric(image_path):
    """Main function to analyze fabric color and suggest correction."""
    colors, original_image = extract_dominant_colors(image_path)

    if len(colors) < 2:
        return {"Message": "Not enough colors detected."}

    dominant_color = colors[0]
    secondary_color = colors[1]
    
    print("Dominant Color (RGB):", dominant_color)  # Print the detected dominant color
    
    dye_solution, corrected_color = suggest_dyeing_solution(dominant_color, secondary_color)

    return {
        "Original Image": original_image,
        "Suggested Dye Formula": dye_solution,
        "Corrected Color": corrected_color
    }

def apply_correction(image, target_color):
    """Apply the corrected color to defect areas in the image."""
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 100])  # Define a threshold for defective areas
    upper_bound = np.array([255, 255, 255])
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)
    corrected_image = image.copy()
    corrected_image[mask > 0] = target_color
    return corrected_image

def visualize_correction(original_image, corrected_color):
    """Generate an image showing before and after correction."""
    corrected_image = apply_correction(original_image, corrected_color)
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original Image")
    axes[0].axis("off")
    
    axes[1].imshow(np.full_like(original_image, corrected_color, dtype=np.uint8))
    axes[1].set_title("Corrected Image")
    axes[1].axis("off")
    
    plt.show()

# Run the program
image_path = open_image()
if image_path:
    result = process_fabric(image_path)
    print("Suggested Dye Formula:", result["Suggested Dye Formula"])
    print("Corrected Color (RGB):", result["Corrected Color"])
    visualize_correction(result["Original Image"], result["Corrected Color"])