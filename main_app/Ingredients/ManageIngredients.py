from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt

class ManageIngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setStyleSheet("background-color: lightgray;")

        layout = QHBoxLayout(self)
        label = QLabel("Manage Ingredients")
        label.setStyleSheet("color: black; font-size: 25px;")
        self.setLayout(layout)

        layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.setContentsMargins(0, 50, 0, 0)