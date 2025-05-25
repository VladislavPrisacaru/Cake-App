from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helper import HelperClass

class AddRecipeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setStyleSheet("background-color: lightgray;")
        self.set_style()

        self.main_layout = QVBoxLayout()
        label = QLabel("Add Recipe")
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 50, 0, 0)
        
        container = self.initUI()
        self.main_layout.addWidget(container)
    
    def initUI(self):
        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        layout.addWidget(QLabel("Recipe Name:"), alignment=Qt.AlignLeft | Qt.AlignTop)

        self.recipe_name, _ = HelperClass.create_labeled_input("Recipe Name:", layout)

        return main_container

    def set_style(self):
        self.setStyleSheet("""
            QLabel {
                color: black; 
                font-size: 25px;}
            """)