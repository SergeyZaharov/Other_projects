import os
import random
import shutil

def prepare_data():
    # Пути к исходным данным
    input_images = "/Users/katasama/Desktop/ITMO CHANGED/dataset/images"
    input_labels = "/Users/katasama/Desktop/ITMO CHANGED/dataset/labels"
    
    # Пути для выходных данных
    output_train_images = "/Users/katasama/Desktop/ITMO CHANGED/dataset/train/images"
    output_train_labels = "/Users/katasama/Desktop/ITMO CHANGED/dataset/train/labels"
    output_val_images = "/Users/katasama/Desktop/ITMO CHANGED/dataset/val/images"
    output_val_labels = "/Users/katasama/Desktop/ITMO CHANGED/dataset/val/labels"
    
    # Создание необходимых директорий
    os.makedirs(output_train_images, exist_ok=True)
    os.makedirs(output_train_labels, exist_ok=True)
    os.makedirs(output_val_images, exist_ok=True)
    os.makedirs(output_val_labels, exist_ok=True)
    
    # Список всех изображений
    image_files = [f for f in os.listdir(input_images) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Перемешивание списка файлов для случайного распределения
    random.seed(1337)
    random.shuffle(image_files)
    
    # Разделение на train и val (например, 90% для train, 10% для val)
    train_ratio = 0.9
    train_size = int(len(image_files) * train_ratio)
    train_files = image_files[:train_size]
    val_files = image_files[train_size:]
    
    def copy_files(file_list, src_images, src_labels, dest_images, dest_labels):
        for file_name in file_list:
            # Копирование изображения
            src_image_path = os.path.join(src_images, file_name)
            shutil.copy(src_image_path, dest_images)
            
            # Копирование соответствующей аннотации
            label_name = os.path.splitext(file_name)[0] + ".txt"
            src_label_path = os.path.join(src_labels, label_name)
            if os.path.exists(src_label_path):
                shutil.copy(src_label_path, dest_labels)
    
    # Копирование файлов для обучающей выборки
    copy_files(train_files, input_images, input_labels, output_train_images, output_train_labels)
    # Копирование файлов для валидационной выборки
    copy_files(val_files, input_images, input_labels, output_val_images, output_val_labels)
    
    print("Данные успешно разделены!")

def copy_additional_labels():
    # Пути к дополнительным аннотациям (если они отделены)
    input_labels_train = "/Users/katasama/Desktop/ITMO CHANGED/dataset/labels/train"
    output_train_labels = "/Users/katasama/Desktop/ITMO CHANGED/dataset/train/labels"
    output_val_labels = "/Users/katasama/Desktop/ITMO CHANGED/dataset/val/labels"
    os.makedirs(output_train_labels, exist_ok=True)
    os.makedirs(output_val_labels, exist_ok=True)
    
    def copy_labels(image_folder, label_folder, output_label_folder):
        for image_file in os.listdir(image_folder):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                label_name = os.path.splitext(image_file)[0] + ".txt"
                src_label_path = os.path.join(label_folder, label_name)
                if os.path.exists(src_label_path):
                    shutil.copy(src_label_path, output_label_folder)
                else:
                    print(f"Warning: No label found for image {image_file}")
    
    train_images_folder = "/Users/katasama/Desktop/ITMO CHANGED/dataset/train/images"
    copy_labels(train_images_folder, input_labels_train, output_train_labels)
    
    val_images_folder = "/Users/katasama/Desktop/ITMO CHANGED/dataset/val/images"
    copy_labels(val_images_folder, input_labels_train, output_val_labels)
    
    print("Аннотации успешно разделены!")
