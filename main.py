import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt
from search_gifs import get_gif_info, save_info_to_txt, load_info_from_txt  # Import functions

class GifDataExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: white;")

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Widgets
        self.gif_label = QLabel("Select a GIF file to display:")
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.gif_label)

        self.gif_display = QLabel()
        self.gif_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.gif_display)

        self.info_display = QTextEdit()
        self.info_display.setReadOnly(False)
        self.layout.addWidget(self.info_display)

        self.load_button = QPushButton("Load GIF")
        self.load_button.clicked.connect(self.load_gif)
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Info to TXT")
        self.save_button.clicked.connect(self.save_info)
        self.layout.addWidget(self.save_button)

        self.txt_file = "gif_info.txt"

    def load_gif(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select GIF File", "", "GIF Files (*.gif);;All Files (*)", options=options)
        if file_name:
            self.display_gif(file_name)
            self.extract_and_display_info(file_name)

    def display_gif(self, file_name):
        self.movie = QMovie(file_name)
        self.gif_display.setMovie(self.movie)
        self.movie.start()

    def extract_and_display_info(self, file_name):
        gif_info = get_gif_info(file_name)
        info_text = json.dumps(gif_info, indent=4)
        self.info_display.setPlainText(info_text)

    def save_info(self):
        info_text = self.info_display.toPlainText()
        gif_info = json.loads(info_text)
        save_info_to_txt(gif_info, self.txt_file)

    def load_info(self):
        gif_info = load_info_from_txt(self.txt_file)
        info_text = json.dumps(gif_info, indent=4)
        self.info_display.setPlainText(info_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifDataExtractor()
    window.show()
    sys.exit(app.exec())