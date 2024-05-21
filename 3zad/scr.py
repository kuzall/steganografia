from scipy.fft import dctn, idctn
from PIL import Image
import numpy as np


# Загружаем изображение
image = Image.open("1234.jpg")

# Преобразуем изображение в массив numpy
image_array = np.array(image)

# Нормализуем значения пикселей в диапазон [0, 1]
normalized_image = image_array / 255.0

# Получаем размеры изображения
height, width, channels = normalized_image.shape

# Размеры блоков
block_size = 4
num_blocks_h = height // block_size
num_blocks_w = width // block_size

# Преобразуем каждый блок 8x8 с помощью дискретного косинусного преобразования (DCT)
scrambled_blocks = np.zeros_like(normalized_image)

for i in range(num_blocks_h):
    for j in range(num_blocks_w):
        block = normalized_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, :]
        dct_block = dctn(block, norm='ortho')
        scrambled_blocks[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, :] = dct_block

# Сохраняем скремблированное изображение для последующего использования
scrambled_image = Image.fromarray((scrambled_blocks * 255).astype(np.uint8))
scrambled_image.save("scrambled_image.jpg")

# Показываем скремблированное изображение
scrambled_image.show()
