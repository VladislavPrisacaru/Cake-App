from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QWidget, QScrollArea, QFrame, QMenu, QWidgetAction, QLineEdit, QComboBox
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

        self._parent = parent
        self.db = parent.db
        
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

        self.add_existing.clicked.connect(self.existing_ingredients_selection)

        add_ingredient_layout.setSpacing(100)
        add_ingredient_layout.setContentsMargins(50, 20, 50, 20)

        layout.addLayout(add_ingredient_layout)

        self.ingredient_box = IngredientBox(self)
        layout.addWidget(self.ingredient_box)


        layout.setContentsMargins(200, 0, 200, 0)
        return main_container
    
    def existing_ingredients_selection(self):
        menu = QMenu(self)

        # Create a scrollable widget
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Add your ingredient buttons/items
        for _, name, *_ in self._parent.db.get_all_ingredients():
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton {background-color: lightgray; font-size: 20px; color: black; padding: 5px;}"
                              "QPushButton:hover {background-color: gray;}")
            scroll_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, n=name: self.ingredient_box.add_ingredient(n))

        scroll_layout.addStretch()

        # Scroll area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMinimumWidth(100)
        scroll_area.setMaximumHeight(300)  

        # Add scroll area to QWidgetAction
        scroll_action = QWidgetAction(menu)
        scroll_action.setDefaultWidget(scroll_area)
        menu.addAction(scroll_action)

        # Show the menu
        menu.exec_(self.add_existing.mapToGlobal(self.add_existing.rect().bottomLeft()))
    
    def include_ingredient(self, name):
        pass

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
                           
            QMenu {
                background-color: white;
                padding: 5px;
                border-radius: 1px;}
            
            QMenu:item {
                background-color: lightgray;
                font-size: 20px;
                color: black;
                padding: 5px;}
                
            QMenu:item:selected {
                background-color: gray;}
            """)

class IngredientBox(QFrame):
    def __init__(self, parent=None):
        super().__init__()
        self.db = parent.db
        self.setMinimumSize(200, 400)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_widget)

        # Final layout for this QFrame (to hold scroll area)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.set_style()

    def add_ingredient(self, name):
        layout = QHBoxLayout()

        date, ing_name, weight, weight_u, price, price_u = self.db.get_chosen_ingredient(name)

        layout.addWidget(QLabel(ing_name))

        weight_edit = QLineEdit()
        weight_edit.setText(f"{weight}")
        layout.addWidget(weight_edit)

        weight_combo = QComboBox()
        weight_combo.addItems(["g", "kg", "ml", "l", "oz", "lb"])
        layout.addWidget(weight_combo)

        row_widget = QWidget()
        row_widget.setLayout(layout)

        # Add to scroll layout
        self.scroll_layout.addWidget(row_widget)
    
    def set_style(self):
        self.setStyleSheet("""
        QWidget {background-color: white; border: 2px solid #07394B;}
            
        QLineEdit {
            padding: 1px;
            border-radius: 4px;
            font-size: 18px;
            color: black;
            background-color: white;}
                           
        QLineEdit:focus {
            border: 1px solid #07394B;}
        
        QLabel {
            color: black; 
            font-size: 20px;}
                           """)

        






