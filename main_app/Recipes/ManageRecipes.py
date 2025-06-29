from PySide6.QtWidgets import (QScrollArea, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
import os

class ManageRecipesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setObjectName("ManageRecipeWidget")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(0, 50, 0, 0)
        self.setLayout(layout)

        # Title label
        title_label = QLabel("Recipe Manager")
        title_label.setObjectName("ManageRecipeLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

    def initUI(self):
        scroll_area = QScrollArea()

        self.container = QWidget(self)

        scroll_area.setWidget(self.container)
    
    def load_recipes(self):
        if hasattr(self, 'grid_layout'): # i think this repositions the items in the grid layout
            for i in reversed(range(self.grid_layout.count())): 
                widget = self.grid_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        else:
            self.grid_layout = QGridLayout()
            self.container.addLayout(self.grid_layout)

        self.grid_layout.setSpacing(5)
        recipes = self.db.get_all_recipes()

        # 3 ingredients per row
        for idx, recipe in enumerate(recipes):
            row = idx // 3
            col = idx % 3
            recipe_widget = Recipe(recipe, self)
            self.grid_layout.addWidget(recipe_widget, row, col)

        

class Recipe(QFrame):
    def __init__(self, recipe, parent=None):
        super().__init__(parent)

        