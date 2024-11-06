import os
from datetime import datetime
import json
from struct import unpack

def read_gif(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

def get_gif_info(file_name):
    gif_data = read_gif(file_name)
    info = {
        "Número de versión": get_version(gif_data),
        "Tamaño de imagen": get_size(gif_data),
        "Cantidad de colores": get_num_colors(gif_data),
        "Tipo de compresión": get_compression(gif_data),
        "Formato numérico": get_format(gif_data),
        "Color de fondo": get_background_color(gif_data),
        "Cantidad de imágenes": get_image_count(gif_data),
        "Fecha de creación": get_creation_date(file_name),
        "Fecha de modificación": get_modification_date(file_name),
        "Comentarios agregados": get_comments(gif_data)
    }
    return info

def get_version(gif_data):
    return gif_data[3:6].decode('ascii')

def get_size(gif_data):
    width = int.from_bytes(gif_data[6:8], 'little')
    height = int.from_bytes(gif_data[8:10], 'little')
    return (width, height)

def get_num_colors(gif_data):
    packed_field = gif_data[10]
    color_table_size = 2 ** ((packed_field & 0b111) + 1)
    return color_table_size

def get_compression(gif_data):
    return "LZW"

def get_format(gif_data):
    # El encabezado tiene información sobre el formato, que es generalmente "GIF87a" o "GIF89a"
    return gif_data[0:6].decode('ascii')

def get_background_color(gif_data):
    return gif_data[11]

def get_image_count(gif_data):
    # El bloque de imágenes comienza después de los encabezados y puede incluir varias imágenes.
    image_count = 0
    index = 13  # Después del encabezado del GIF
    while index < len(gif_data):
        if gif_data[index] == 0x2C:  # Identificador de imagen
            image_count += 1
            index += 9 + unpack('<H', gif_data[index + 4:index + 6])[0] * unpack('<H', gif_data[index + 6:index + 8])[0]
        elif gif_data[index] == 0x21:  # Extensión de bloque (podría ser para comentarios)
            index += 2 + unpack('<B', gif_data[index + 1:index + 2])[0]
        else:
            break
    return image_count

def get_creation_date(file_name):
    creation_time = os.path.getctime(file_name)
    return datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

def get_modification_date(file_name):
    modification_time = os.path.getmtime(file_name)
    return datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

def get_comments(gif_data):
    comments = []
    index = 13  # Después del encabezado del GIF
    while index < len(gif_data):
        if gif_data[index] == 0x21:  # Bloques de extensión
            block_type = gif_data[index + 1]
            if block_type == 0xFE:  # Bloque de comentario
                comment_length = gif_data[index + 2]
                comment = gif_data[index + 3 : index + 3 + comment_length].decode('ascii', errors='ignore')
                comments.append(comment)
            index += 2 + gif_data[index + 1]
        else:
            break
    return comments

def save_info_to_txt(info, txt_file):
    with open(txt_file, 'w') as f:
        json.dump(info, f, indent=4)

def load_info_from_txt(txt_file):
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            return json.load(f)
    return {}
