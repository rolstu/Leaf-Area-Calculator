# Necessary imports
import tkinter as tk
from tkinter import ttk  # Import ttk module for the progress bar
from tkinter import filedialog
import pandas as pd
import cv2
import os
import numpy as np
from PIL import Image

def run_script():
    # Get the image directory and CSV save path from the user interface
    image_dir = entry_image_dir.get()
    save_path = entry_save_path.get()

    # Calculate the total number of images to be processed for the progress bar
    total_images = sum(1 for filename in os.listdir(image_dir)
                       if filename.endswith(('.jpg', '.jpeg', '.tif')))
    progress_bar['maximum'] = total_images
    progress_bar['value'] = 0

    # List to store the results of the calculated areas
    results = []

    # Loop through all files in the specified directory
    for filename in os.listdir(image_dir):
        # Accept only image files with specific extensions
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.tif'):
            # Read the image using OpenCV
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply binary threshold
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

            # Find contours in the image
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours by minimum area
            min_area = 100
            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

            # Calculate the total filtered area
            total_area = np.sum([cv2.contourArea(cnt) for cnt in filtered_contours])

            # Calculation of the area in cm2 (assuming certain conversions and PPI values)
            ppi = 300  # Assume a fixed PPI value for the example
            area_cm = total_area * (2.54 / ppi)**2

            # Store the results
            results.append({
                'filename': filename,
                'area_cm2': area_cm
            })

            # Update the progress bar for each processed image
            progress_bar['value'] += 1
            root.update_idletasks()

    # Convert the results into a pandas DataFrame and save it as CSV
    df = pd.DataFrame(results)
    df.to_csv(save_path, index=False)

    # Display success message
    label_result.config(text="Successfully executed!")

# User interface setup
root = tk.Tk()
root.geometry("400x250")  # Adjusted window size to accommodate progress bar
root.title("Leaf Area Calculator")

# Create and arrange widgets
label_image_dir = tk.Label(root, text="Image Directory:")
label_image_dir.pack()
entry_image_dir = tk.Entry(root)
entry_image_dir.pack()

label_save_path = tk.Label(root, text="CSV Save Path:")
label_save_path.pack()
entry_save_path = tk.Entry(root)
entry_save_path.pack()

button_run = tk.Button(root, text="Run", command=run_script)
button_run.pack()

# Initialize and pack the progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack()

label_result = tk.Label(root, text="")
label_result.pack()

# Start the application
root.mainloop()