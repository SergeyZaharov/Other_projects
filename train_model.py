from ultralytics import YOLO

def train():
    model_dir = '/Users/katasama/Desktop/ITMO CHANGED/model/'
    data_yaml = '/Users/katasama/Desktop/ITMO CHANGED/dataset/data.yaml'
    # Загружаем предобученную модель YOLOv8n
    model_path = model_dir + 'yolov8n.pt'
    model = YOLO(model_path)
    
    # Запускаем обучение с указанными параметрами
    results = model.train(
        data=data_yaml,
        imgsz=416,
        epochs=100,
        batch=16,
        name='helmet_run_100_epoches',
        project=model_dir
    )
    print("Обучение завершено!")
