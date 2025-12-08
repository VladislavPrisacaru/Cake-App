from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
import os

class AddSalesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setStyleSheet("background-color: lightgray;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(0, 50, 0, 0)
        self.setLayout(layout)

        # Title label
        title_label = QLabel("Add Sales")
        title_label.setStyleSheet("color: black; font-size: 25px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        image_path = os.path.join(project_root, "high_felix.jpg")

        pixmap = QPixmap(image_path)

        scaled_pixmap = pixmap.scaled(750, 950, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label)
        