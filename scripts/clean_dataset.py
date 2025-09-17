"""
Данный код создает файл duplicates.csv, который включает в себя пары похожих изображений и расстояние между ними
"""

import os
from PIL import Image
import imagehash
import pandas as pd
from tqdm import tqdm

IMGS_DIR = r"C:\Users\asdfu\Downloads\data_for_sirius_2025\data_sirius"
OUTPUT_CSV = "duplicates_g.csv"

#threshold - порог "расстояния", которое записывается в файл
def find_duplicates(IMGS_DIR, hash_func=imagehash.phash, threshold=5):
    hashes = {}
    duplicates = {}

    files = os.listdir(IMGS_DIR) #получаем все изображения из директории IMGS_DIR

    for f in tqdm(files, desc="Hashing images"):
        path = os.path.join(IMGS_DIR, f)
        try:
            img = Image.open(path)
            h = hash_func(img)
            hashes[f] = h
        except Exception as e:
            print(f"Ошибка при {f}: {e}")
    print(f"Обработано файлов: {len(files)}")

    # ищем похожие и записываем в словарь
    n = len(files)
    for i in tqdm(range(n), desc="Comparing"):
        for j in range(i + 1, n):
            f1, f2 = files[i], files[j]
            if f1 in hashes and f2 in hashes:
                dist = hashes[f1] - hashes[f2]
                if dist <= threshold:
                    duplicates.setdefault(f1, []).append((f2, dist))

    return duplicates


duplicates = find_duplicates(IMGS_DIR)

rows = []
for f1, matches in duplicates.items():
    for f2, dist in matches:
        rows.append({"file1": f1, "file2": f2, "distance": dist})

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
print(f"Найдено {len(rows)} пар дубликатов, результат сохранен в {OUTPUT_CSV}")
