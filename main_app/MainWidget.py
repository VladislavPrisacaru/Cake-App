from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setStyleSheet("background-color: lightgray;")

        layout = QHBoxLayout(self)
        label = QLabel("Welcome to Cake MD")
        label.setStyleSheet("color: black; font-size: 25px;")
        self.setLayout(layout)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 50, 0, 0)

        