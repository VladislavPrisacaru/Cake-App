from PySide6.QtWidgets import (QScrollArea, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from Database import db
import os
from Helper import HelperClass
from collections import defaultdict

class ManageRecipesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setObjectName("ManageRecipeWidget")

        self._parent = parent
        self.db = db

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setContentsMargins(0, 50, 0, 0)
        self.setLayout(self.main_layout)

        # Title label
        title_label = QLabel("Recipe Manager")
        title_label.setObjectName("ManageRecipeLabel")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        self.initUI()

        self.create_scroll_grid()
        self.load_recipes()
    
    def create_scroll_grid(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("IngredientScrollArea")
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add these lines to ensure proper background handling
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.scroll_container = QWidget()
        self.scroll_container.setObjectName("IngredientScrollContainer")
        self.scroll_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Set a transparent background policy
        self.scroll_container.setAttribute(Qt.WA_TranslucentBackground)
        self.scroll_area.setAttribute(Qt.WA_TranslucentBackground)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # Add some margins
        self.scroll_container.setLayout(self.grid_layout)
        
        self.scroll_area.setWidget(self.scroll_container)
        self.main_layout.addWidget(self.scroll_area)

    def initUI(self):
        pass
    
    def load_recipes(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        recipes = self.db.get_all_recipes()
        grouped_recipes = defaultdict(list)

        for row in recipes:
            recipe_name = row[0]
            grouped_recipes[recipe_name].append(row[1:])

        for idx, (recipe_name, ingredients) in enumerate(grouped_recipes.items()):
            row = idx // 3
            col = idx % 3
            recipe_widget = self.load_recipe(recipe_name, ingredients)
            self.grid_layout.addWidget(recipe_widget, row, col)
    
    def load_recipe(self, recipe_name, ingredients):
        text = f"<b>{recipe_name}</b><br><br>"

        for ingredient in ingredients:
            ingredient_name, used_weight, used_unit, stock_weight, stock_unit, price, price_unit = ingredient
            
            text += (
                f"Ingredient: {ingredient_name}<br>"
                f"&nbsp;&nbsp;&nbsp;•Weight: {used_weight}{used_unit}"
                f"&nbsp;&nbsp;&nbsp;•Price: {price_unit}{price}<br></html>")
            
        recipe_btn = HelperClass.AnimatedLabel((255, 255, 255),(13, 74, 98),(0, 0, 0),(255, 255, 255))
  
        recipe_btn.setText(f"<html>{text}</html>")

        return recipe_btn

        

class Recipe(QFrame):
    def __init__(self, recipe_name, ingredients, parent=None):
        super().__init__(parent)

        text = f"<b>{recipe_name}</b><br><br>"

        for ingredient in ingredients:
            ingredient_name, used_weight, used_unit, stock_weight, stock_unit, price, price_unit = ingredient
            
            text += (
                f"Ingredient: {ingredient_name}<br>"
                f"&nbsp;&nbsp;&nbsp;•Weight: {used_weight}{used_unit}<br>"
                f"&nbsp;&nbsp;&nbsp;•Price: {price_unit}{price}</html>")
            
        recipe_btn = HelperClass.AnimatedLabel((255, 255, 255),(13, 74, 98),(0, 0, 0),(255, 255, 255))
        recipe_btn.setText(f"<html>{text}</html>")
        #recipe_btn.setMaximumHeight(100)


        