from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QScrollArea, QLineEdit, QComboBox, QFrame, QGridLayout
from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from Database import db
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helper import HelperClass, signals

class AddIngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("AddIngredientsWidget")

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.db = db
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        label = QLabel("Ingredients Overview")
        label.setObjectName("HeaderLabel")

        self.main_layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 20, 0, 30)

        self.add_btn()

        self.overlay = QWidget(self) # create an overlay widget
        self.overlay.setObjectName("Overlay")
        self.overlay.hide()
        
        self.modal_widget = GetIngredients(parent=self)
        self.modal_widget.hide()

        self.create_scroll_grid()
        self.load_ingredients()

    def add_btn(self):
        # add ingredient button at the top
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 20)

        add_btn = QPushButton("Add Ingredient")
        add_btn.setObjectName("AddIngredientBtn")
        add_btn.setMinimumWidth(500)
        add_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout.addStretch() # so its at teh center of the screen
        layout.addWidget(add_btn)
        layout.addStretch()

        self.main_layout.addLayout(layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        add_btn.clicked.connect(lambda: self.show_modal("add"))
    
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

    def load_ingredients(self):
        for i in range(3):
            self.grid_layout.setColumnStretch(i, 1)

        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        ingredients = self.db.get_all_ingredients()

        for idx, ingredient in enumerate(ingredients):
            row = idx // 3
            col = idx % 3
            ingredient_widget = self.load_ingredient(ingredient)
            self.grid_layout.addWidget(ingredient_widget, row, col)
    
    def load_ingredient(self, ingredient):
        date, name, weight, weight_unit, price, price_unit = ingredient
        ingredient_btn = HelperClass.AnimatedLabel((255, 255, 255),(13, 74, 98),(0, 0, 0),(255, 255, 255))
        ingredient_btn.setText(f"<html><b>{name}</b><br>"
                                f"Weight: {weight}{weight_unit}<br>"
                                f"Price: {price_unit}{price}</html>")
        ingredient_btn.setMaximumHeight(100)
        
        #allow to edit or delete the existing ingredient
        ingredient_btn.mousePressEvent = lambda event: self.show_modal("edit", ingredient)

        return ingredient_btn

    def show_modal(self, mode="add", ingredient=None):
        # set the overlay to cover the entire main window
        main_window = self.parent().parent()
        self.overlay.setGeometry(0, 0, main_window.width(), main_window.height())
        self.overlay.show()
        self.overlay.raise_()
        
        # Configure the existing modal widget based on mode
        self.modal_widget.set_mode(mode, ingredient)
        
        # Position and show the modal in the centre
        self.modal_widget.setGeometry(
            (self.width() - self.modal_widget.width()) // 2,
            (self.height() - self.modal_widget.height()) // 2,
            self.modal_widget.width(),
            self.modal_widget.height()
        )
        self.modal_widget.show()
        self.modal_widget.raise_()

    def hide_modal(self):
        # Hide the overlay and modal widget
        self.overlay.hide()
        self.modal_widget.hide()

class GetIngredients(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GetIngredientModal")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.initUI()
        self.adjustSize()

        self.db = db
        
        # Set initial mode
        self.set_mode("add")

    def set_mode(self, mode, ingredient=None):
        self.mode = mode
        self.current_ingredient = ingredient
        
        # Update UI based on mode
        if mode == "add":
            self.title_label.setText("Add Ingredient")
            self.delete_btn.hide()
            self.save_btn.setText("Save")
            self.reset_inputs()

        elif mode == "edit":
            self.title_label.setText("Edit Ingredient")
            self.delete_btn.show()
            self.save_btn.setText("Update")
            self.populate_inputs()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        
        # Title label
        self.title_label = QLabel("Add Ingredient")
        self.title_label.setObjectName("TitleLabel")
        #self.title_label.setStyleSheet("color: black; font-size: 30px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Input fields
        self.ing_name, _, name_label = HelperClass.create_labeled_input("Ingredient Name:", self.layout, place_holder_text="e.g. Flour, Sugar, etc.")
        self.ing_weight, self.ing_weight_unit, weight_label = HelperClass.create_labeled_input("Ingredient Weight:", self.layout, ["g", "kg", "ml", "l", "oz", "lb"])
        self.ing_price, self.ing_price_unit, price_label = HelperClass.create_labeled_input("Ingredient Price:", self.layout, ["£", "€", "$"])

        self.ing_name.setObjectName("ModalEdits")
        self.ing_weight.setObjectName("ModalEdits")
        self.ing_price.setObjectName("ModalEdits")

        self.ing_weight_unit.setObjectName("UnitCombos")
        self.ing_price_unit.setObjectName("UnitCombos")

        name_label.setObjectName("ModalLabels")
        weight_label.setObjectName("ModalLabels")
        price_label.setObjectName("ModalLabels")

        # Initialize buttons
        self.save_btn = QPushButton("Save")
        self.delete_btn = QPushButton("Delete")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.setObjectName("ModalBtns")
        self.delete_btn.setObjectName("ModalBtns")
        self.cancel_btn.setObjectName("ModalBtns")
        
        # Connect signals
        self.cancel_btn.clicked.connect(self.cancel_event)
        self.delete_btn.clicked.connect(self.delete_event)
        self.save_btn.clicked.connect(self.save_event)

        # Button layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.save_btn)
        self.buttons_layout.addWidget(self.delete_btn)
        self.buttons_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.buttons_layout)

        self.layout.setSpacing(10)
        self.setMinimumWidth(300)
        self.setMinimumHeight(400)
        
        return self.layout

    def populate_inputs(self):
        # populate the input fields with the current ingredient data when in edit mode
        if self.current_ingredient:
            date, name, weight, weight_unit, price, price_unit = self.current_ingredient
            self.ing_name.setText(name)
            self.ing_weight.setText(str(weight))
            self.ing_weight_unit.setCurrentText(weight_unit)
            self.ing_price.setText(str(price))
            self.ing_price_unit.setCurrentText(price_unit)

    def cancel_event(self): # the cancel button
        self.reset_inputs()
        self.parent().hide_modal()

    def save_event(self): # the save button
        # get the ingredient values
        name = self.ing_name.text()
        weight = self.ing_weight.text()
        price = self.ing_price.text()
        weight_unit = self.ing_weight_unit.currentText()
        price_unit = self.ing_price_unit.currentText()

        name = name.title()

        if not name or not weight or not price:
            return

        #save or update ingredient in the database based on mode
        if self.mode == "add":
            self.db.add_ingredient(name, weight, weight_unit, price, price_unit)
        elif self.mode == "edit" and self.current_ingredient:
            old_name = self.current_ingredient[1]
            self.db.update_ingredient(old_name, name, weight, weight_unit, price, price_unit)

        self.parent().load_ingredients()  # Refresh the list
        self.reset_inputs()
        self.parent().hide_modal()
        signals.ingredient_added.emit()

    def delete_event(self):
        if not self.current_ingredient:
            return

        name = self.current_ingredient[1]
        self.db.delete_ingredient(name)
        self.parent().load_ingredients()  # Refresh the list
        self.reset_inputs()
        self.parent().hide_modal()
        signals.ingredient_deleted.emit()

    def reset_inputs(self):
        self.ing_weight.setText("")
        self.ing_price.setText("")
        self.ing_name.setText("")
        self.ing_weight_unit.setCurrentIndex(0)
        self.ing_price_unit.setCurrentIndex(0)