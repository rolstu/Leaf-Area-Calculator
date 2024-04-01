# Importaciones necesarias
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import cv2
import os
import numpy as np
from PIL import Image

def run_script():
    # Obtener el directorio de las imágenes y la ruta de guardado del CSV desde la interfaz de usuario
    image_dir = entry_image_dir.get()
    save_path = entry_save_path.get()

    # Lista para almacenar los resultados de las áreas calculadas
    results = []

    # Recorrer todos los archivos en el directorio especificado
    for filename in os.listdir(image_dir):
        # Aceptar solo archivos de imagen con extensiones específicas
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.tif'):
            # Leer la imagen utilizando OpenCV
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)

            # Convertir la imagen a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Aplicar umbral binario
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

            # Encontrar contornos en la imagen
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filtrar contornos por área mínima
            min_area = 100
            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

            # Calcular el área total filtrada
            total_area = np.sum([cv2.contourArea(cnt) for cnt in filtered_contours])

            # Cálculo del área en cm2 (asumiendo ciertas conversiones y valores de PPI)
            # Nota: Este paso puede necesitar ajustes dependiendo de las especificaciones reales de las imágenes
            ppi = 300  # Asumir un valor fijo de PPI para el ejemplo
            area_cm = total_area * (2.54 / ppi)**2

            # Almacenar los resultados
            results.append({
                'filename': filename,
                'area_cm2': area_cm
            })

    # Convertir los resultados en un DataFrame de pandas y guardarlo como CSV
    df = pd.DataFrame(results)
    df.to_csv(save_path, index=False)

    # Mostrar mensaje de éxito
    label_result.config(text="¡Ejecutado con éxito!")

# Configuración de la interfaz de usuario
root = tk.Tk()
root.geometry("400x200")
root.title("Calculadora masiva de SLA")

# Crear y organizar widgets
label_image_dir = tk.Label(root, text="Directorio de Imágenes:")
label_image_dir.pack()
entry_image_dir = tk.Entry(root)
entry_image_dir.pack()

label_save_path = tk.Label(root, text="Ruta de Guardado del CSV:")
label_save_path.pack()
entry_save_path = tk.Entry(root)
entry_save_path.pack()

button_run = tk.Button(root, text="Ejecutar", command=run_script)
button_run.pack()

label_result = tk.Label(root, text="")
label_result.pack()

# Iniciar la aplicación
root.mainloop()
