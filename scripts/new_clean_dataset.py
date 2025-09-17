"""
Данный код является логическим продолжением файла clean_dataset.py,
по файлу duplicates.csv удаляет только те изображения,
"расстояние" между которыми 0.
"""

import os
import shutil
import pandas as pd

DUPLICATES_FILE = "duplicates.csv"
ORIG_DIR = r"C:\Users\asdfu\Downloads\data_for_sirius_2025\data_sirius"
CLEAN_DIR = r"C:\Users\asdfu\OneDrive\Desktop\clean_data"


data = pd.read_csv(DUPLICATES_FILE)
data = data[data["distance"] == 0] #отбор полных дубликатов
remove = set(data["file2"].tolist())

print(remove)
print(f"Найдено полных дубликатов: {len(remove)}")


if os.path.exists(CLEAN_DIR):
    print(f"Папка {CLEAN_DIR} уже существует")
else:
    shutil.copytree(ORIG_DIR, CLEAN_DIR)
    print(f"Копия датасета создана")

    removed = 0
    for f in remove:
        target_path = os.path.join(CLEAN_DIR, f)
        if os.path.exists(target_path):
            os.remove(target_path)
            removed += 1

    print(f"Удалено {removed} файлов-дубликатов")
