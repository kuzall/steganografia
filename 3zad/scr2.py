from scipy.fft import dctn
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
block_size = 8
num_blocks_h = height // block_size
num_blocks_w = width // block_size

# Коэффициент квантования
quantization_factor = 1

# Коэффициенты квантования с затуханием
quantization_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]])

# Преобразуем каждый блок 8x8 с помощью дискретного косинусного преобразования (DCT)
scrambled_blocks = np.zeros_like(normalized_image)

for i in range(num_blocks_h):
    for j in range(num_blocks_w):
        block = normalized_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, :]
        dct_block = dctn(block, norm='ortho')
        
        # Применяем квантование с затуханием к каждому каналу
        quantized_dct_block = np.round(dct_block / quantization_factor)
        
        scrambled_blocks[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, :] = quantized_dct_block

# Сохраняем скремблированное изображение для последующего использования
scrambled_image = Image.fromarray((scrambled_blocks * 255).astype(np.uint8))

# Показываем скремблированное изображение
scrambled_image.show()
