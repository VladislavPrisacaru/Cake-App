from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QFrame, QMenu, QWidgetAction, QLineEdit, QComboBox, QSizePolicy
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

class IngredientBox(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self.db = parent.db
        self.setMinimumSize(200, 400)
        
        self.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")
        self.setWidget(self.content_widget)
        
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.addStretch()

        self.set_style()

    def add_ingredient(self, name):
        # Get data from DB
        date, ing_name, weight, weight_u, price, price_u = self.db.get_chosen_ingredient(name)
        
        row_widget = QWidget()
        row_widget.setObjectName("rowWidget")
        row_widget.setMaximumHeight(50)
        
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(10, 5, 10, 5)
        row_layout.setSpacing(20)
        
        label = QLabel(ing_name)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        row_layout.addWidget(label)
        
        weight_edit = QLineEdit()
        weight_edit.setText(f"{weight}")
        weight_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row_layout.addWidget(weight_edit)
        
        weight_combo = QComboBox()
        weight_combo.addItems(["g", "kg", "ml", "l", "oz", "lb"])
        weight_combo.setStyleSheet("background-color: white; color: black; font-size: 18px;")
        weight_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        row_layout.addWidget(weight_combo)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        row_layout.addWidget(delete_btn)

        delete_btn.clicked.connect(lambda checked, r=row_widget: self.delete_row(r))
        
        # Add row widget to main layout
        self.main_layout.insertWidget(0, row_widget)
        
    def delete_row(self, row):
        row.deleteLater()
    
    def set_style(self):
        style = """            
            QLineEdit {
                padding: 3px;
                border-radius: 4px;
                font-size: 20px;
                color: black;
                background-color: white;
                border: 1px solid #ccc;
            }
            
            QLineEdit:focus {
                border: 1px solid #07394B;
            }
            
            QLabel {
                color: black; 
                font-size: 20px;
                border: None;
                min-width: 100px;
                background-color: white;
                border-radius: 5px;
                padding-left: 3px;
            }
            
            QPushButton#deleteBtn {
                background-color: #b80617;
                color: white;
                border: none;
                padding: 5px 10px;
                min-width: 60px;
                border-radius: 5px;
            }
            
            QPushButton#deleteBtn:pressed {
                background-color: #9e0514;
            }

            QPushButton#deleteBtn:hover {
                background-color: #cc0404;
            }
            
            QComboBox {
                padding: 3px;
                font-size: 18px;
                min-width: 60px;
                color: black;
                background-color: white;
            }

            QComboBox::drop-down {
                color:black;
            }
            QScrollArea {
                background-color: white;
                border: 2px solid #07394B;
            }
            QWidget#contentWidget {
                background-color: white;
            }
            QWidget#rowWidget {
                background-color: lightgray;
                border-radius: 5px;
            }
        """
        self.setStyleSheet(style)

        






