import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def buscar_gifs(carpeta):
    gifs_encontrados = []
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.lower().endswith('.gif'):
                gifs_encontrados.append(os.path.join(root, file))
    return gifs_encontrados

def leer_gif(ruta_gif):
    with open(ruta_gif, 'rb') as f:
        return f.read()

def obtener_version(gif_data):
    return gif_data[3:6].decode('ascii')

def obtener_tamaño(gif_data):
    width = int.from_bytes(gif_data[6:8], 'little')
    height = int.from_bytes(gif_data[8:10], 'little')
    return (width, height)

def obtener_num_colores(gif_data):
    packed_field = gif_data[10]
    color_table_size = 2 ** ((packed_field & 0b111) + 1)  # 2^(N+1)
    return color_table_size

def obtener_compresion(gif_data):
    return "LZW"

def obtener_formato_numerico(gif_data):
    return "P"

def obtener_color_fondo(gif_data):
    background_color_index = gif_data[11]
    return background_color_index

def contar_imagenes(gif_data):
    count = 0
    index = 13
    while index < len(gif_data):
        if gif_data[index] == 0x2C:
            count += 1
            index += 9
            lzw_min_code_size = gif_data[index]
            index += 1
            while True:
                block_size = gif_data[index]
                index += 1
                if block_size == 0:
                    break
                index += block_size
        else:
            index += 1
    return count

def obtener_info_gif(ruta_gif):
    gif_data = leer_gif(ruta_gif)
    return {
        "Versión": obtener_version(gif_data),
        "Tamaño": obtener_tamaño(gif_data),
        "Número de Colores": obtener_num_colores(gif_data),
        "Compresión": obtener_compresion(gif_data),
        "Formato Numérico": obtener_formato_numerico(gif_data),
        "Color de Fondo": obtener_color_fondo(gif_data),
        "Número de Imágenes": contar_imagenes(gif_data)
    }

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        gifs = buscar_gifs(carpeta)
        if gifs:
            lista_gifs.delete(0, tk.END)
            for gif in gifs:
                lista_gifs.insert(tk.END, gif)
                info = obtener_info_gif(gif)
                print(f"Información para {gif}: {info}")
            messagebox.showinfo("Búsqueda completada", f"Se encontraron {len(gifs)} archivos GIF.")
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron archivos GIF en esta carpeta.")

ventana = tk.Tk()
ventana.title("Buscador de archivos GIF")

etiqueta = tk.Label(ventana, text="Seleccione una carpeta para buscar archivos GIF:")
etiqueta.pack(pady=10)

boton_buscar = tk.Button(ventana, text="Seleccionar carpeta", command=elegir_carpeta)
boton_buscar.pack(pady=5)

lista_gifs = tk.Listbox(ventana, width=80, height=20)
lista_gifs.pack(pady=10)

ventana.mainloop()