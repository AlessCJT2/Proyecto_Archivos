import os
from datetime import datetime
import json

def read_gif(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

def get_gif_info(file_name):
    gif_data = read_gif(file_name)
    info = {
        "Path": file_name,
        "Version": get_version(gif_data),
        "Size": get_size(gif_data),
        "Number of Colors": get_num_colors(gif_data),
        "Compression": get_compression(gif_data),
        "Background Color": get_background_color(gif_data),
        "Creation Date": get_creation_date(file_name),
        "Modification Date": get_modification_date(file_name)
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

def get_background_color(gif_data):
    return gif_data[11]

def get_creation_date(file_name):
    creation_time = os.path.getctime(file_name)
    return datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

def get_modification_date(file_name):
    modification_time = os.path.getmtime(file_name)
    return datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

def save_info_to_txt(info, txt_file):
    with open(txt_file, 'w') as f:
        json.dump(info, f, indent=4)

def load_info_from_txt(txt_file):
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            return json.load(f)
    return {}