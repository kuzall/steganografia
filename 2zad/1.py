import cv2
import numpy as np
import os

# Запрашиваем путь к файлу
image_path = input('Enter the path to the image file: ')

# Проверяем существование файла
if not os.path.exists(image_path):
    print("File doesn't exist.")
    exit()

# Загружаем изображение
image = cv2.imread(image_path)

# Преобразуем изображение в массив пикселей
pixels = np.array(image)

# Вычисляем сумму значений пикселей в каждом канале
channel_sums = np.sum(pixels, axis=(0, 1))

# Находим индекс канала с наибольшей суммой
max_channel_index = np.argmax(channel_sums)

# Выбираем канал с наибольшей суммой для хранения сообщения
channel = pixels[:, :, max_channel_index]

# Запрашиваем сообщение для сокрытия
message = input('Enter the message to hide: ')

# Проверяем, что сообщение можно спрятать в изображение
if len(message) * 8 > channel.size:
    print("Message too long to hide in the image.")
    exit()

# Преобразуем сообщение в биты
message_bits = ''.join([format(ord(c), '08b') for c in message])

# Запрашиваем имя нового файла
new_image_path = input('Enter the name of the new image file: ')

# Записываем биты сообщения в младшие биты пикселей
for i in range(len(message_bits)):
    pixel = channel.flat[i]
    pixel_bits = format(pixel, '08b')
    pixel_bits = pixel_bits[:-1] + message_bits[i]
    channel.flat[i] = int(pixel_bits, 2)

# Заменяем выбранный канал в изображении
pixels[:, :, max_channel_index] = channel

# Преобразуем массив пикселей обратно в изображение
new_image = cv2.merge([pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]])

# Сохраняем новое изображение
cv2.imwrite(new_image_path, new_image)

print('The new image file has been saved.')
