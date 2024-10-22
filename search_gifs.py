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

def obtener_version(gif_path):
    with Image.open(gif_path) as img:
        return img.format_version

def obtener_tamaño(gif_path):
    with Image.open(gif_path) as img:
        return img.size

def obtener_num_colores(gif_path):
    with Image.open(gif_path) as img:
        return len(img.getcolors(maxcolors=256)) if img.mode == 'P' else "N/A"

def obtener_compresion(gif_path):
    with Image.open(gif_path) as img:
        return img.info.get('compression', 'N/A')

def obtener_formato_numerico(gif_path):
    with Image.open(gif_path) as img:
        return img.mode

def obtener_color_fondo(gif_path):
    with Image.open(gif_path) as img:
        return img.info.get('background', 'N/A')

def contar_imagenes(gif_path):
    with Image.open(gif_path) as img:
        return sum(1 for _ in ImageSequence.Iterator(img))

def obtener_info_gif(gif_path):
    return {
        "Versión": obtener_version(gif_path),
        "Tamaño": obtener_tamaño(gif_path),
        "Número de Colores": obtener_num_colores(gif_path),
        "Compresión": obtener_compresion(gif_path),
        "Formato Numérico": obtener_formato_numerico(gif_path),
        "Color de Fondo": obtener_color_fondo(gif_path),
        "Número de Imágenes": contar_imagenes(gif_path)
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
                print(f"Información para {gif}: {info}")  # Imprimir o manejar la info según sea necesario
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
