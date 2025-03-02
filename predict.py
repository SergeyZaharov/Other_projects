import cv2
from ultralytics import YOLO
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def analyze_image():
    # Диалог выбора файла изображения
    filepath = filedialog.askopenfilename(
        title="Выберите изображение", 
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if not filepath:
        return
    model_dir = '/Users/katasama/Desktop/ITMO CHANGED/model/'
    checkpoint_path = f'{model_dir}/helmet_run_100_epoches/weights/best.pt'
    model = YOLO(checkpoint_path)
    
    image = cv2.imread(filepath)
    if image is None:
        messagebox.showerror("Ошибка", "Не удалось загрузить изображение")
        return
    
    results = model.predict(image)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label_text = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(image, label_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    
    output_dir = '/Users/katasama/Desktop/ITMO CHANGED/dataset/test_results/'
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(filepath)
    output_path = os.path.join(output_dir, "analyzed_" + base_name)
    cv2.imwrite(output_path, image)
    
    # Создаем новое окно для показа результата
    top = tk.Toplevel()
    top.title("Анализ изображения")
    cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=pil_img)
    label = tk.Label(top, image=imgtk)
    label.image = imgtk  # сохраняем ссылку
    label.pack()
    
    close_btn = tk.Button(top, text="Закрыть", command=top.destroy)
    close_btn.pack(pady=5)
    
    messagebox.showinfo("Анализ", f"Изображение проанализировано и сохранено в {output_path}")

def analyze_video():
    # Диалог выбора файла видео
    filepath = filedialog.askopenfilename(
        title="Выберите видео", 
        filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
    )
    if not filepath:
        return
    model_dir = '/Users/katasama/Desktop/ITMO CHANGED/model/'
    checkpoint_path = f'{model_dir}/helmet_run_100_epoches/weights/best.pt'
    model = YOLO(checkpoint_path)
    
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        messagebox.showerror("Ошибка", "Не удалось открыть видео")
        return
    
    output_dir = '/Users/katasama/Desktop/ITMO CHANGED/dataset/test_results/'
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(filepath)
    output_path = os.path.join(output_dir, "analyzed_" + base_name.rsplit('.',1)[0] + ".mp4")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label_text = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, label_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        out.write(frame)
    
    cap.release()
    out.release()
    
    # Показываем окно с сообщением о сохранении результата
    top = tk.Toplevel()
    top.title("Анализ видео")
    msg = tk.Label(top, text=f"Видео проанализировано и сохранено в {output_path}")
    msg.pack(pady=5)
    close_btn = tk.Button(top, text="Закрыть", command=top.destroy)
    close_btn.pack(pady=5)
