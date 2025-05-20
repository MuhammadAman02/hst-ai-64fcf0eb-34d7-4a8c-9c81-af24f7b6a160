import cv2
import numpy as np
from skimage import color

def get_dominant_color(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to RGB color space
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to be a list of pixels
    pixels = img_rgb.reshape((-1, 3))
    
    # Convert to float
    pixels = np.float32(pixels)
    
    # Define criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    
    # Perform k-means clustering
    _, labels, palette = cv2.kmeans(pixels, 5, None, criteria, 10, flags)
    
    # Convert to LAB color space
    palette_lab = color.rgb2lab(palette.reshape(1, -1, 3)).reshape(-1, 3)
    
    # Find the cluster with the highest L value (brightness)
    dominant_color = palette[np.argmax(palette_lab[:, 0])]
    
    return dominant_color

def get_color_recommendations(image_path):
    dominant_color = get_dominant_color(image_path)
    
    # Convert dominant color to HSV
    dominant_hsv = color.rgb2hsv(dominant_color.reshape(1, 1, 3)).flatten()
    
    # Define color recommendations based on the dominant color's hue
    hue = dominant_hsv[0]
    
    if 0 <= hue < 0.08:  # Red
        return ["Green", "Blue", "Purple"]
    elif 0.08 <= hue < 0.17:  # Orange
        return ["Blue", "Green", "Purple"]
    elif 0.17 <= hue < 0.33:  # Yellow
        return ["Purple", "Blue", "Green"]
    elif 0.33 <= hue < 0.5:  # Green
        return ["Red", "Purple", "Orange"]
    elif 0.5 <= hue < 0.67:  # Blue
        return ["Orange", "Yellow", "Red"]
    elif 0.67 <= hue < 0.83:  # Indigo
        return ["Yellow", "Orange", "Red"]
    else:  # Violet
        return ["Yellow", "Green", "Orange"]