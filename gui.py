import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import platform

import camera_inference
import predict

def connect_camera():
    camera_inference.run_camera_gui()

def analyze_photo():
    predict.analyze_image()

def analyze_video():
    predict.analyze_video()

def open_analysis_folder():
    folder_path = "dataset/test_results/"
    # Получаем абсолютный путь
    folder_abs = os.path.abspath(folder_path)
    
    try:
        if platform.system() == "Windows":
            subprocess.call(["explorer", folder_abs])
        else:
            subprocess.call(["open", folder_abs])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть папку: {e}")

root = tk.Tk()
root.title("ИКИСИЗ")

btn_camera = tk.Button(root, text="Подключить камеру", command=connect_camera)
btn_camera.pack(pady=5)

btn_photo = tk.Button(root, text="Предложить анализ фотографии", command=analyze_photo)
btn_photo.pack(pady=5)

btn_video = tk.Button(root, text="Предложить анализ видео", command=analyze_video)
btn_video.pack(pady=5)

btn_open = tk.Button(root, text="Открыть папку с анализом", command=open_analysis_folder)
btn_open.pack(pady=5)

root.mainloop()
