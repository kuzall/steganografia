import chardet

def binary_to_text(binary):
    text_result = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text_result += chr(int(byte, 2))
    return text_result

def text_to_binary(text):
    binary_result = ''.join(format(ord(char), '08b') for char in text)
    return binary_result

def remove_trailing_spaces(filename):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            file.write(line.rstrip() + '\n')
        file.truncate()


def add_spaces_to_file(filename, binary_string):
    # Удаляем конечные пробелы перед записью новых данных
    remove_trailing_spaces(filename)

    # Определяем кодировку файла
    with open(filename, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']

    with open(filename, 'r', encoding=encoding) as file:
        lines = file.readlines()

    # Создаем новый список строк с добавленными пробелами
    new_lines = []
    for i in range(len(binary_string)):
        line = lines[i].rstrip('\n')  # Удаляем символ переноса строки
        if binary_string[i] == '0':
            line += ' '
        elif binary_string[i] == '1':
            line += '  '
        new_lines.append(line + '\n')

    # Дополняем новый список строк, если остались строки в исходном файле
    if len(lines) > len(binary_string):
        new_lines.extend(lines[len(binary_string):])

    # Создаем новый файл для записи с той же кодировкой
    new_filename = filename.split('.')[0] + '_modified.txt'
    with open(new_filename, 'w', encoding=encoding) as new_file:
        new_file.writelines(new_lines)


def decode_binary(binary_string):
    decoded_message = binary_to_text(binary_string)
    return decoded_message

def count_trailing_spaces(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        trailing_spaces_binary = ""
        for line in file:
            count = len(line) - len(line.rstrip())
            trailing_spaces_binary += '0' if count == 2 else '1' if count == 3 else ''

    print("Binary string:", trailing_spaces_binary)

    # Декодируем бинарную строку в текст и выводим декодированную строку
    decoded_text = decode_binary(trailing_spaces_binary)
    print("Decoded text:", decoded_text)




def modify_file_with_text():
    # Выбор: добавить пробелы к файлу или декодировать сообщение
    choice = input("Что вы хотите сделать: добавить пробелы к файлу (1) или декодировать сообщение (2)? ")

    if choice == '1':
        # Запрос пути к файлу
        filename = input("Введите путь к файлу: ")

        # Запрос сообщения
        text = input("Введите сообщение: ")

        # Преобразование текста в бинарную строку
        binary_string = text_to_binary(text)

        # Добавление пробелов в файл
        add_spaces_to_file(filename, binary_string)

        print("Пробелы успешно добавлены к файлу.")
    elif choice == '2':
        filename = input("Введите путь к файлу для декодирования сообщения: ")
        count_trailing_spaces(filename)
    else:
        print("Некорректный выбор.")

# Пример использования:
modify_file_with_text()
