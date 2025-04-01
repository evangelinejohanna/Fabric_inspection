import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Function to read the JSON file and get the stored image path
def load_defect_results(json_path="defect_results.json"):
    with open(json_path, "r") as file:
        data = json.load(file)
    return data["image_path"], data["defect_type"]

# Function to extract dominant colors from the image
def extract_dominant_colors(image_path, k=2):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_.astype(int)

    return [tuple(color) for color in colors], cv2.imread(image_path)

# Convert RGB to LAB color space
def rgb_to_lab(color):
    color_array = np.uint8([[color]])
    lab_color = cv2.cvtColor(color_array, cv2.COLOR_RGB2LAB)[0][0]
    return lab_color

# Convert LAB back to RGB
def lab_to_rgb(color):
    color_array = np.uint8([[color]])
    rgb_color = cv2.cvtColor(color_array, cv2.COLOR_LAB2RGB)[0][0]
    return tuple(rgb_color)

# Function to suggest a dyeing solution
def suggest_dyeing_solution(dominant_color, secondary_color):
    dominant_lab = rgb_to_lab(dominant_color)
    secondary_lab = rgb_to_lab(secondary_color)
    
    color_shift = dominant_lab - secondary_lab
    corrected_lab = secondary_lab + color_shift
    corrected_lab = np.clip(corrected_lab, 0, 255)
    corrected_rgb = lab_to_rgb(corrected_lab)

    dye_formula = {
        "L Adjustment": color_shift[0],
        "A Adjustment": color_shift[1],
        "B Adjustment": color_shift[2]
    }

    return dye_formula, corrected_rgb

# Function to process fabric image
def process_fabric(image_path):
    colors, original_image = extract_dominant_colors(image_path)

    if len(colors) < 2:
        return {"Message": "Not enough colors detected."}

    dominant_color = colors[0]
    secondary_color = colors[1]
    
    print("Dominant Color (RGB):", dominant_color)

    dye_solution, corrected_color = suggest_dyeing_solution(dominant_color, secondary_color)

    return {
        "Original Image": original_image,
        "Suggested Dye Formula": dye_solution,
        "Corrected Color": corrected_color
    }

# Function to apply color correction
def apply_correction(image, target_color):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 100])
    upper_bound = np.array([255, 255, 255])
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)
    corrected_image = image.copy()
    corrected_image[mask > 0] = target_color
    return corrected_image

# Function to visualize before and after correction
def visualize_correction(original_image, corrected_color):
    corrected_image = apply_correction(original_image, corrected_color)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    axes[1].imshow(np.full_like(original_image, corrected_color, dtype=np.uint8))
    axes[1].set_title("Corrected Image")
    axes[1].axis("off")

    plt.show()

# Load image path from JSON and process
image_path, defect_type = load_defect_results()
print(f"Processing defect: {defect_type}")

if image_path:
    result = process_fabric(image_path)
    print("Suggested Dye Formula:", result["Suggested Dye Formula"])
    print("Corrected Color (RGB):", result["Corrected Color"])
    visualize_correction(result["Original Image"], result["Corrected Color"])
