from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from Database import DatabaseManager

class IngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.add_btn()

    def add_btn(self):
        layout = QHBoxLayout()

        add_btn = QPushButton("Add Ingredient")
        add_btn.setMinimumWidth(500)
        add_btn.setStyleSheet(
            "QPushButton {background-color: #07394B; color: white; font-size: 16px; border: none; padding: 15px; border-radius: 25px;}"
            "QPushButton:hover {background-color: #0D4A62}"
            "QPushButton:pressed {background-color: #052B38}")
        add_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        layout.addStretch()
        layout.addWidget(add_btn)
        layout.addStretch()

        self.main_layout.addLayout(layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        add_btn.clicked.connect(self.set_ingredient_info)

    def set_ingredient_info(self):
        pass