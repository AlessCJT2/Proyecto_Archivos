import os
import tkinter as tk
from tkinter import filedialog, messagebox

def buscar_gifs(carpeta):
    gifs_encontrados = []
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.lower().endswith('.gif'):
                gifs_encontrados.append(os.path.join(root, file))
    return gifs_encontrados

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        gifs = buscar_gifs(carpeta)
        if gifs:
            lista_gifs.delete(0, tk.END)
            for gif in gifs:
                lista_gifs.insert(tk.END, gif)
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
