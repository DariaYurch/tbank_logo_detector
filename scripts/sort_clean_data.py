"""
Данный код использовался для сортировки очищенных исходных данных на основе базовой
модели, чтобы в дальнейшем сформировать новую обучающую выборку без дисбаланса классов
"""

import os
import shutil
from ultralytics import YOLO
from tqdm import tqdm

batch_size = 250

DATA_DIR = r"C:\Users\asdfu\OneDrive\Desktop\clean_data"
OUTPUT_DIR = r"C:\Users\asdfu\OneDrive\Desktop\labeled_data"


os.makedirs(os.path.join(OUTPUT_DIR, "0"), exist_ok=True) #папка со всеми негативными изображениями (лого не найден)
os.makedirs(os.path.join(OUTPUT_DIR, "1"), exist_ok=True) #папка со всеми положительными изображениями (лого найден)

model = YOLO("data/best_8.pt")

image_files = []
for root, _, files in os.walk(DATA_DIR):
    for f in files:
        image_files.append(os.path.join(root, f))

print(f"Найдено {len(image_files)} изображений для сортировки") #проверка корректно найденной директории


for i in range(0, len(image_files), batch_size):
    batch_files = image_files[i:i+batch_size]

    results = model.predict(
        source=batch_files,
        conf=0.7,
        save=False,
        stream=True,
        batch=1
    )

    for r in tqdm(results, total=len(batch_files), desc=f"Batch {i//batch_size+1}"):
        img_path = r.path
        img_name = os.path.basename(img_path)

        if len(r.boxes) > 0:
            shutil.copy(img_path, os.path.join(OUTPUT_DIR, "1", img_name))
        else:
            shutil.copy(img_path, os.path.join(OUTPUT_DIR, "0", img_name))

print("Сортировка завершена")