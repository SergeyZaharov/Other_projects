from ultralytics import YOLO

def finetune():
    model_dir = '/Users/katasama/Desktop/ITMO CHANGED/model/'
    data_yaml = '/Users/katasama/Desktop/ITMO CHANGED/dataset/data.yaml'
    
    # Путь к чекпоинту последнего обучения
    checkpoint_path = f'{model_dir}/helmet_run_100_epoches/weights/last.pt'
    
    # Загружаем модель из чекпоинта
    model = YOLO(checkpoint_path)
    
    # Дообучение модели (например, 1 эпоха)
    results = model.train(
        data=data_yaml,
        imgsz=416,
        epochs=1,
        batch=16,
        name='helmet_finetune',
        project=model_dir,
        resume=False  # Начинаем новое обучение с чекпоинта
    )
    print("Дообучение завершено!")
