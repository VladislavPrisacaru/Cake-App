from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class OptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setStyleSheet("background-color: lightgray;")

        layout = QVBoxLayout(self)
        label = QLabel("Options")
        self.setStyleSheet(" QLabel{color: black; font-size: 25px;}")
        self.setLayout(layout)

        layout.addWidget(label)
        layout.setContentsMargins(0, 50, 0, 0)
        layout.addWidget(QLabel("Scale"))
        layout.addWidget(QLabel("Theme"))
        layout.addStretch()