import cv2
import tkinter as tk
from ultralytics import YOLO
import os
from PIL import Image, ImageTk

def run_camera_gui(camera_index=0):
    model_dir = '/Users/katasama/Desktop/ITMO CHANGED/model/'
    checkpoint_path = f'{model_dir}/helmet_run_100_epoches/weights/best.pt'
    model = YOLO(checkpoint_path)
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Ошибка: не удалось открыть камеру с индексом {camera_index}")
        return

    # Создаем новое окно Tkinter для отображения видеопотока
    cam_window = tk.Toplevel()
    cam_window.title("Камера YOLO Inference")
    
    # Метка для отображения кадра
    lbl = tk.Label(cam_window)
    lbl.pack()
    
    # Создаем папку для записи, если её нет
    output_folder = '/Users/katasama/Desktop/ITMO CHANGED/cam_test'
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "itmo_rezult_mishs.mp4")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    running = [True]  # Флаг для остановки цикла обновления кадров
    
    def update_frame():
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось считать кадр")
            cam_window.after(10, update_frame)
            return
        
        # Выполнение предсказания для кадра
        results = model.predict(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label_text = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label_text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Запись кадра в видеофайл
        out.write(frame)
        # Конвертация кадра для отображения в Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
        
        if running[0]:
            cam_window.after(10, update_frame)
    
    def stop_camera(event=None):
        running[0] = False
        cap.release()
        out.release()
        cam_window.destroy()
        print(f"Видео сохранено в {output_path}")
    
    # Привязываем клавишу ESC к функции остановки камеры
    cam_window.bind('<Escape>', stop_camera)
    
    update_frame()

if __name__ == '__main__':
    root = tk.Tk()
    run_camera_gui()
    root.mainloop()
