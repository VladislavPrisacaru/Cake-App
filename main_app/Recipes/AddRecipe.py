from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QWidget, QScrollArea, QFrame
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
        
        self.main_layout = QVBoxLayout()
        label = QLabel("Add Recipe")
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 50, 0, 0)
        
        container = self.initUI()
        self.main_layout.addWidget(container, alignment=Qt.AlignTop)
        self.main_layout.addStretch()
        self.set_style()

    def initUI(self):
        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        self.recipe_name, _, self.label = HelperClass.create_labeled_input("Recipe Name:", layout)
        self.recipe_name.setMaxLength(50)
        layout.addWidget(QLabel("Ingredients:"))

        add_ingredient_layout = QHBoxLayout()

        self.add_new = QPushButton("Add New Ingredient")
        self.add_existing = QPushButton("Add Existing Ingredient")

        add_ingredient_layout.addWidget(self.add_new)
        add_ingredient_layout.addWidget(self.add_existing)

        add_ingredient_layout.setSpacing(100)
        add_ingredient_layout.setContentsMargins(50, 20, 50, 20)

        layout.addLayout(add_ingredient_layout)

        ingredient_box = IngredientBox()
        layout.addWidget(ingredient_box)


        layout.setContentsMargins(200, 0, 200, 0)
        return main_container

    def set_style(self):
        self.setStyleSheet("""
            QLabel {
                color: black; 
                font-size: 25px;}
                           
            QLineEdit {
                padding: 2px;
                border-radius: 4px;
                font-size: 22px;}
                           
            QLineEdit:focus {
                border: 1px solid #07394B;}
            
            QPushButton {background-color: #07394B; color: white; font-size: 22px; border: none; padding: 7px; border-radius: 15px;}
            QPushButton:hover {background-color: #0D4A62}
            QPushButton:pressed {background-color: #052B38}
            """)

class IngredientBox(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(200, 300)

