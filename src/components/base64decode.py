import base64


def fix_base64_padding(base64_data):
    if base64_data is None:
        return None

    try:
        # Если base64_data уже bytes, не добавляем символы "="
        if isinstance(base64_data, bytes):
            decoded_data = base64.b64decode(base64_data)
        else:
            # Добавляем символы "=" для правильного декодирования
            missing_padding = len(base64_data) % 4
            if missing_padding != 0:
                base64_data += '=' * (4 - missing_padding)

            # Декодируем Base64 строку в бинарные данные
            decoded_data = base64.b64decode(base64_data)

        return decoded_data
    except Exception as e:
        print(f"Error decoding Base64: {e}")
        return None