import chardet

def read_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        text = raw_data.decode(encoding)
        return text

def write_to_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def count_replaceable_chars(container):
    count = 0
    for char in container:
        if char in ['а', 'о']:
            count += 1
    return count

def embed_message(container, message):
    replaceable_chars_count = count_replaceable_chars(container)
    max_message_length = replaceable_chars_count // 8
    print("Максимальное количество сообщений, которые можно встроить:", max_message_length)

    start_marker = "1111111111"
    end_marker = "1111111111"

    binary_message = f"{start_marker}{''.join(format(ord(c), '08b') for c in message)}{end_marker}"

    embedded_text = ""
    for char in container:
        if char in ['а', 'о'] and binary_message:
            if binary_message[0] == '0':
                embedded_text += 'a' if char == 'а' else 'o'
            else:
                embedded_text += 'а' if char == 'а' else 'о'
            binary_message = binary_message[1:]
        else:
            embedded_text += char

    return embedded_text

def extract_message(container):
    start_marker = "1111111111"
    end_marker = "1111111111"

    binary_message = ""
    for char in container:
        if char in ['а', 'о', 'a', 'o']:
            binary_message += '0' if char in ['a', 'o'] else '1'

    binary_message_with_markers = binary_message

    start_index = binary_message_with_markers.find(start_marker)
    end_index = binary_message_with_markers.find(end_marker, start_index + len(start_marker))

    if start_index != -1 and end_index != -1:
        binary_message = binary_message_with_markers[start_index + len(start_marker):end_index]

    extracted_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        extracted_message += chr(int(byte, 2))

    return extracted_message

action = input("Выберите действие: зашифровать (encode) или расшифровать (decode)? ")

if action.lower() == "encode":
    container_file = input("Введите путь к чистому файлу-контейнеру: ")
    output_file = input("Введите путь к выходному файлу: ")

    container_text = read_file(container_file)
    replaceable_chars_count = count_replaceable_chars(container_text)
    max_message_length = replaceable_chars_count // 8
    print("Максимальное количество сообщений, которые можно встроить:", max_message_length)

    message = input("Введите сообщение, которое нужно спрятать: ")
    if len(message) > max_message_length:
        print("Слишком длинное сообщение. Выберите другое сообщение.")
    else:
        embedded_text = embed_message(container_text, message)
        write_to_file(output_file, embedded_text)
        print("Текст после встраивания сохранен в файле:", output_file)

elif action.lower() == "decode":
    container_file = input("Введите путь к файлу-контейнеру с зашифрованным сообщением: ")
    container_text = read_file(container_file)
    extracted_message = extract_message(container_text)
    print("Извлеченное сообщение:", extracted_message)

else:
    print("Неверный ввод. Пожалуйста, выберите 'encode' или 'decode'.")
