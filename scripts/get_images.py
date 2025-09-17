"""
Данный код использовался для генерации случайной подвыборки
"""
import os
import random
import shutil

n = 3000

main_dr = r'C:\Users\asdfu\Downloads\data_for_sirius_2025\data_sirius'
copy_dr = r'C:\Users\asdfu\OneDrive\Desktop\data'

os.makedirs(copy_dr, exist_ok=True)

images = os.listdir(main_dr)
random_images = random.sample(images, 3000)


for i in random_images:
    shutil.copy(os.path.join(main_dr, i), os.path.join(copy_dr, i))

print(f"Готово, было скопировано {len(random_images)} изображений")





