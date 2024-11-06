import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtCore import Qt
from search_gifs import get_gif_info, save_info_to_txt

class GifExtractorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Extractor de Datos de GIF")
        self.setGeometry(100, 100, 700, 500)

        # Estilo de la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f9;
                color: #333;
            }
            QLabel {
                color: #4a90e2;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #357ab7;
            }
            QPushButton:pressed {
                background-color: #2c5b91;
            }
        """)

        self.layout = QVBoxLayout()

        # Etiqueta para mostrar el GIF
        self.gif_label = QLabel("Selecciona un archivo GIF", self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.gif_label)

        # Botón para cargar GIF
        self.load_button = QPushButton("Cargar GIF", self)
        self.load_button.clicked.connect(self.load_gif)
        self.layout.addWidget(self.load_button)

        # Área de texto para mostrar los datos extraídos
        self.info_text = QTextEdit(self)
        self.info_text.setReadOnly(True)
        self.layout.addWidget(self.info_text)

        # Área de texto para agregar comentarios
        self.comment_text = QTextEdit(self)
        self.comment_text.setPlaceholderText("Escribe tus comentarios aquí...")
        self.layout.addWidget(self.comment_text)

        # Botón para guardar la información en un archivo TXT
        self.save_button = QPushButton("Guardar Información en TXT", self)
        self.save_button.clicked.connect(self.save_info)
        self.layout.addWidget(self.save_button)

        # Botón para agregar comentarios al GIF
        self.add_comment_button = QPushButton("Agregar Comentarios", self)
        self.add_comment_button.clicked.connect(self.add_comment)
        self.layout.addWidget(self.add_comment_button)

        self.setLayout(self.layout)

    def load_gif(self):
        # Cargar un archivo GIF
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo GIF", "", "Archivos GIF (*.gif)")
        if file_name:
            # Extraer información del GIF
            self.gif_info = get_gif_info(file_name)
            self.display_info()

            # Mostrar el GIF en el QLabel
            self.gif_label.setPixmap(QPixmap(file_name).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

            # Guardar la ruta del GIF
            self.gif_path = file_name

    def display_info(self):
        # Mostrar los datos extraídos en la interfaz gráfica
        info = "\n".join([f"<font color='#4a90e2'><b>{key}:</b></font> <font color='#333'>{value}</font>" for key, value in self.gif_info.items()])
        self.info_text.setHtml(info)

    def save_info(self):
        # Guardar la información en un archivo TXT
        if hasattr(self, 'gif_info') and hasattr(self, 'gif_path'):
            # Obtener la carpeta donde se encuentra el GIF
            gif_directory = os.path.dirname(self.gif_path)

            # Definir la ruta completa para guardar el archivo
            output_path = os.path.join(gif_directory, "datos_gif.txt")

            # Guardar la información en el archivo de texto
            save_info_to_txt(self.gif_info, output_path)

            # Mostrar mensaje en la interfaz
            self.info_text.append(f"<font color='#4a90e2'><b>Información guardada en '{output_path}'.</b></font>")

    def add_comment(self):
        # Agregar comentarios al archivo de información
        comment = self.comment_text.toPlainText()
        if comment:
            if hasattr(self, 'gif_info'):
                if "Comentarios agregados" not in self.gif_info:
                    self.gif_info["Comentarios agregados"] = []
                self.gif_info["Comentarios agregados"].append(comment)
                self.info_text.append(f"<font color='#4a90e2'><b>Comentario agregado:</b></font> <font color='#333'>{comment}</font>")
                self.comment_text.clear()
            else:
                self.info_text.append("<font color='#ff0000'><b>Primero carga un archivo GIF.</b></font>")
        else:
            self.info_text.append("<font color='#ff0000'><b>Por favor escribe un comentario.</b></font>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifExtractorApp()
    window.show()
    sys.exit(app.exec())



