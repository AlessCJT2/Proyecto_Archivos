import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt
from search_gifs import get_gif_info, save_info_to_txt  # Importa la función de guardar

class GifDataExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: white;")

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Etiqueta para mostrar el GIF
        self.gif_display = QLabel("Select a GIF file to display:")
        self.gif_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.gif_display)

        # Área de texto para mostrar información del GIF
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.layout.addWidget(self.info_display)

        # Botón para cargar el GIF
        self.load_button = QPushButton("Load GIF")
        self.load_button.clicked.connect(self.load_gif)
        self.layout.addWidget(self.load_button)

        # Botón para guardar la información
        self.save_button = QPushButton("Save Info to TXT")
        self.save_button.clicked.connect(self.save_info)
        self.layout.addWidget(self.save_button)

        # Variable para almacenar la ruta actual del GIF
        self.current_gif_path = ""

    def load_gif(self):
        try:
            # Abre el diálogo para seleccionar un archivo GIF
            file_name, _ = QFileDialog.getOpenFileName(self, "Select GIF File", "", "GIF Files (*.gif);;All Files (*)")
            if file_name:
                self.current_gif_path = file_name
                self.display_gif(file_name)
                self.extract_and_display_info(file_name)
        except Exception as e:
            self.info_display.setPlainText(f"Error al cargar el GIF: {e}")

    def display_gif(self, file_name):
        try:
            # Muestra el GIF seleccionado en la interfaz
            self.movie = QMovie(file_name)
            self.gif_display.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            self.info_display.setPlainText(f"Error al mostrar el GIF: {e}")

    def extract_and_display_info(self, file_name):
        try:
            # Extrae información del GIF y la muestra en el área de texto
            gif_info = get_gif_info(file_name)
            info_text = json.dumps(gif_info, indent=4)
            self.info_display.setPlainText(info_text)
        except Exception as e:
            self.info_display.setPlainText(f"Error al extraer información del GIF: {e}")

    def save_info(self):
        if self.current_gif_path:
            try:
                # Obtiene el directorio del archivo GIF seleccionado
                gif_directory = os.path.dirname(self.current_gif_path)
                output_path = os.path.join(gif_directory, "datos_gifs.txt")

                # Guarda la información del GIF en un archivo de texto
                info_text = self.info_display.toPlainText()
                gif_info = json.loads(info_text)  # Convierte a JSON para asegurar que es un formato válido
                save_info_to_txt(gif_info, output_path)
                self.info_display.append(f"\nInformación guardada en: {output_path}")
            except json.JSONDecodeError:
                self.info_display.append("\nError: La información no está en formato JSON.")
            except Exception as e:
                self.info_display.append(f"\nError al guardar la información: {e}")
        else:
            self.info_display.append("\nNo se ha cargado ningún GIF.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifDataExtractor()
    window.show()
    sys.exit(app.exec())

