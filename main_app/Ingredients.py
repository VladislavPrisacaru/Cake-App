from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QComboBox, QFrame, QGridLayout
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from Database import DatabaseManager
from Animations import fade_in_animation

db = DatabaseManager("cakeshop.db")

class IngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.add_btn()

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.overlay.hide()

        self.modal_widget = GetIngredients(self)
        self.modal_widget.hide()

        self.load_ingredients()
        #self.ingredient_list = LoadIngredient(self)

    def add_btn(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)

        add_btn = QPushButton("Add Ingredient")
        add_btn.setMinimumWidth(500)
        add_btn.setStyleSheet(
            "QPushButton {background-color: #07394B; color: white; font-size: 16px; border: none; padding: 15px; border-radius: 25px;}"         
            "QPushButton:hover { background-color: #0D4A62 }"
            "QPushButton:pressed { background-color: #052B38 }" )
        add_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout.addStretch()
        layout.addWidget(add_btn)
        layout.addStretch()

        self.main_layout.addLayout(layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        add_btn.clicked.connect(self.show_modal)

    def load_ingredients(self):
        ingredients = db.get_all_ingredients()

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.grid_layout.setSpacing(20)

        for idx, ingredient in enumerate(ingredients):
            idx = self.grid_layout.count() 
            row = idx // 3
            col = idx % 3
            ingredient_widget = LoadIngredient(self, ingredient)
            self.grid_layout.addWidget(ingredient_widget, row, col)

    def show_modal(self):
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.show()
        self.overlay.raise_()

        self.modal_widget.setGeometry(
            (self.width() - self.modal_widget.width()) // 2,
            (self.height() - self.modal_widget.height()) // 2,
            self.modal_widget.width(),
            self.modal_widget.height()
        )
        self.modal_widget.show()
        self.modal_widget.raise_()

    def hide_modal(self):
        self.overlay.hide()
        self.modal_widget.hide()

    def resizeEvent(self, event):
        """Handle window resizing to keep overlay and modal properly positioned"""
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.width(), self.height())
            self.modal_widget.move(
                self.width() // 2 - self.modal_widget.width() // 2,
                self.height() // 2 - self.modal_widget.height() // 2
            )
        super().resizeEvent(event)
    

class GetIngredients(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightgray; border-radius: 10px; padding: 4px;")
        layout = self.initUI()
        self.setLayout(layout)
        self.adjustSize()
        self.set_style()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        label = QLabel("Add Ingredient")
        label.setStyleSheet("color: black; font-size: 30px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.ing_name, _  = self.create_labeled_input("Ingredient Name:", place_holder_text="e.g. Flour, Sugar, etc.")
        self.ing_weight, self.ing_weight_unit = self.create_labeled_input("Ingredient Weight:", ["g", "kg", "ml", "l", "oz", "lb"])
        self.ing_price, self.ing_price_unit = self.create_labeled_input("Ingredient Price:", ["£", "€", "$"])

        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        save_btn = QPushButton("Save")
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        self.layout.addLayout(buttons_layout)

        self.layout.setSpacing(10)

        cancel_btn.clicked.connect(self.cancel_event)
        save_btn.clicked.connect(self.save_event)

        return self.layout
    
    def create_labeled_input(self, label_text, combo_items=None, place_holder_text=None):
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        label.setStyleSheet("color: black; font-size: 20px;")
        layout.addWidget(label)

        input_layout = QHBoxLayout()
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(place_holder_text)
        line_edit.setMaxLength(30)


        if label_text == "Name":
            regex = QRegularExpression("[a-zA-Z0-9 ]*")
            validator = QRegularExpressionValidator(regex, self)
            line_edit.setValidator(validator)
        elif label_text == "Ingredient Weight:" or label_text == "Ingredient Price:":
            validator = QDoubleValidator(0.0, 9999.99, 2, self)
            validator.setNotation(QDoubleValidator.StandardNotation)
            line_edit.setValidator(validator)

        line_edit.setStyleSheet("background-color: white; color: black;")
        input_layout.addWidget(line_edit)

        combo_box = None
        if combo_items:
            combo_box = QComboBox()
            combo_box.addItems(combo_items)
            combo_box.setStyleSheet("background-color: white; color: black; font-size: 13px;")
            input_layout.addWidget(combo_box)

        layout.addLayout(input_layout)
        self.layout.addLayout(layout)

        return line_edit, combo_box

    def cancel_event(self): 
        self.ing_weight.setText("")
        self.ing_price.setText("")
        self.ing_name.setText("")
        self.ing_weight_unit.setCurrentIndex(0)
        self.ing_price_unit.setCurrentIndex(0)
        self.parent().hide_modal()

    def save_event(self):
        name = self.ing_name.text()
        weight = self.ing_weight.text()
        price = self.ing_price.text()
        weight_unit = self.ing_weight_unit.currentText()
        price_unit = self.ing_price_unit.currentText()

        if not name or not weight or not price:
            return

        db.add_ingredient(name, weight, weight_unit, price, price_unit)

        ingredient = db.get_chosen_ingredient(name)
        if ingredient:
            ingredient = LoadIngredient(self.parent(), ingredient)
            self.parent().grid_layout.addWidget(ingredient)

        self.ing_weight.setText("")
        self.ing_price.setText("")
        self.ing_name.setText("")
        self.ing_weight_unit.setCurrentIndex(0)
        self.ing_price_unit.setCurrentIndex(0)
        
        self.parent().hide_modal()

    def set_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: lightgray;
                border-radius: 8px;
                padding: 4px;
            }
                                   
            QLineEdit {
                padding: 1px;
            
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #07394B;
            }
                        
            
            QPushButton {background-color: #07394B; color: white; font-size: 18px; border: none; padding: 4px; border-radius: 15px;}      
            QPushButton:hover { background-color: #0D4A62 }
            QPushButton:pressed { background-color: #052B38 }
                           
        """)

class LoadIngredient(QFrame):
    def __init__(self, parent=None, ingredient=None):
        super().__init__(parent)
        #self.setStyleSheet("background-color: white ; border-radius: 8px; padding: 4px;")
        self.ingredient = ingredient
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        if not self.ingredient:
            return

        date, name, weight, weight_unit, price, price_unit = self.ingredient
        ingredient_btn = QPushButton(f"{name} \n {weight} {weight_unit} - {price} {price_unit}")
        ingredient_btn.setStyleSheet("QPushButton {color: black; font-size: 20px; background-color: white ; border-radius: 8px; padding: 10px;}"
                                     "QPushButton:hover {background-color: #0D4A62;}")
        layout.addWidget(ingredient_btn)
        
        self.setLayout(layout)




"""
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QComboBox, QFrame, QGridLayout
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from Database import DatabaseManager
from Animations import fade_in_animation

db = DatabaseManager("cakeshop.db")

class IngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.add_btn()

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.overlay.hide()

        self.load_ingredients()
        #self.ingredient_list = LoadIngredient(self)

    def add_btn(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)

        add_btn = QPushButton("Add Ingredient")
        add_btn.setMinimumWidth(500)
        add_btn.setStyleSheet(
            "QPushButton {background-color: #07394B; color: white; font-size: 16px; border: none; padding: 15px; border-radius: 25px;}"         
            "QPushButton:hover { background-color: #0D4A62 }"
            "QPushButton:pressed { background-color: #052B38 }" )
        add_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout.addStretch()
        layout.addWidget(add_btn)
        layout.addStretch()

        self.main_layout.addLayout(layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        add_btn.clicked.connect(self.show_modal)

    def load_ingredients(self):
        ingredients = db.get_all_ingredients()

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.grid_layout.setSpacing(8)

        for idx, ingredient in enumerate(ingredients):
            idx = self.grid_layout.count() 
            row = idx // 3
            col = idx % 3
            ingredient_widget = LoadIngredient(self, ingredient)
            self.grid_layout.addWidget(ingredient_widget, row, col)

    def show_modal(self, mode="normal", ingredient=None):
        # if self.modal_widget:
        #     self.modal_widget.deleteLater()

        self.modal_widget = GetIngredients(self, mode=mode, ingredient=ingredient)
        self.modal_widget.hide()
        
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.show()
        self.overlay.raise_()

        self.modal_widget.adjustSize()
        self.modal_widget.setGeometry(
            (self.width() - self.modal_widget.width()) // 2,
            (self.height() - self.modal_widget.height()) // 2,
            self.modal_widget.width(),
            self.modal_widget.height()
        )
        self.modal_widget.show()
        self.modal_widget.raise_()

    def hide_modal(self):
        self.overlay.hide()
        self.modal_widget.hide()

    def resizeEvent(self, event):
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.width(), self.height())
            self.modal_widget.move(
                self.width() // 2 - self.modal_widget.width() // 2,
                self.height() // 2 - self.modal_widget.height() // 2
            )
        super().resizeEvent(event)
    

class GetIngredients(QFrame):
    def __init__(self, parent=None, mode="normal", ingredient=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightgray; border-radius: 10px; padding: 4px;")
        self.mode = mode
        self.ingredient = ingredient
        layout = self.initUI()
        self.setLayout(layout)
        self.adjustSize()
        self.set_style()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        if self.mode == "normal":
            label = QLabel("Add Ingredient")
        elif self.mode == "edit":
            label = QLabel("Edit Ingredient")
        else:
            label = QLabel("unknown mode")

        label.setStyleSheet("color: black; font-size: 30px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.ing_name, _  = self.create_labeled_input("Ingredient Name:", place_holder_text="e.g. Flour, Sugar, etc.")
        self.ing_weight, self.ing_weight_unit = self.create_labeled_input("Ingredient Weight:", ["g", "kg", "ml", "l", "oz", "lb"])
        self.ing_price, self.ing_price_unit = self.create_labeled_input("Ingredient Price:", ["£", "€", "$"])

        buttons_layout = QHBoxLayout()

        if self.mode == "normal":
            cancel_btn = QPushButton("Cancel")
            save_btn = QPushButton("Save")
            
            buttons_layout.addWidget(cancel_btn)
            buttons_layout.addWidget(save_btn)
            self.layout.addLayout(buttons_layout)

            self.layout.setSpacing(10)

            cancel_btn.clicked.connect(self.cancel_event)
            save_btn.clicked.connect(self.save_event)

        elif self.mode == "edit":
            cancel_btn = QPushButton("Cancel")
            delete_btn = QPushButton("Delete")
            save_btn = QPushButton("Update")

            buttons_layout.addWidget(cancel_btn)
            buttons_layout.addWidget(delete_btn)
            buttons_layout.addWidget(save_btn)
            self.layout.addLayout(buttons_layout)

            self.populate_inputs()

            self.layout.setSpacing(10)

            cancel_btn.clicked.connect(self.cancel_event)
            delete_btn.clicked.connect(self.delete_event)
            #save_btn.clicked.connect(self.update_event)

        return self.layout

    def populate_inputs(self):
        if self.ingredient:
            name, weight, weight_unit, price, price_unit = self.ingredient[1:]
            self.ing_name.setText(name)
            self.ing_weight.setText(str(weight))
            self.ing_weight_unit.setCurrentText(weight_unit)
            self.ing_price.setText(str(price))
            self.ing_price_unit.setCurrentText(price_unit)
    
    def create_labeled_input(self, label_text, combo_items=None, place_holder_text=None):
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        label.setStyleSheet("color: black; font-size: 20px;")
        layout.addWidget(label)

        input_layout = QHBoxLayout()
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(place_holder_text)
        line_edit.setMaxLength(30)


        if label_text == "Ingredient Name:":
            regex = QRegularExpression("[a-zA-Z0-9 ]*")
            validator = QRegularExpressionValidator(regex, self)
            line_edit.setValidator(validator)
        elif label_text == "Ingredient Weight:" or label_text == "Ingredient Price:":
            validator = QDoubleValidator(0.0, 9999.99, 2, self)
            validator.setNotation(QDoubleValidator.StandardNotation)
            line_edit.setValidator(validator)

        line_edit.setStyleSheet("background-color: white; color: black;")
        input_layout.addWidget(line_edit)

        combo_box = None
        if combo_items:
            combo_box = QComboBox()
            combo_box.addItems(combo_items)
            combo_box.setStyleSheet("background-color: white; color: black; font-size: 13px;")
            input_layout.addWidget(combo_box)

        layout.addLayout(input_layout)
        self.layout.addLayout(layout)

        return line_edit, combo_box

    def cancel_event(self): 
        self.reset_inputs()
        self.parent().hide_modal()

    def save_event(self):
        name = self.ing_name.text()
        weight = self.ing_weight.text()
        price = self.ing_price.text()
        weight_unit = self.ing_weight_unit.currentText()
        price_unit = self.ing_price_unit.currentText()

        if not name or not weight or not price:
            return

        db.add_ingredient(name, weight, weight_unit, price, price_unit)

        ingredient = db.get_chosen_ingredient(name)
        if ingredient:
            ingredient = LoadIngredient(self.parent(), ingredient)
            self.parent().grid_layout.addWidget(ingredient)

        self.reset_inputs()
        self.parent().hide_modal()

    def delete_event(self):
        name = self.ing_name.text()
        if not name:
            return

        db.delete_ingredient(name)

        for i in range(self.parent().grid_layout.count()):
            widget = self.parent().grid_layout.itemAt(i).widget()
            if isinstance(widget, LoadIngredient) and widget.ingredient[1] == name:
                self.parent().grid_layout.removeWidget(widget)
                widget.deleteLater()
                break

        self.reset_inputs()

        self.parent().hide_modal()

    def reset_inputs(self):
        self.ing_weight.setText("")
        self.ing_price.setText("")
        self.ing_name.setText("")
        self.ing_weight_unit.setCurrentIndex(0)
        self.ing_price_unit.setCurrentIndex(0)

    def set_style(self):
        self.setStyleSheet("
            "QFrame {"
                "background-color: lightgray;"
                "border-radius: 8px;"
                "padding: 4px;"
            "}"
                                   
            "QLineEdit {"
                "padding: 1px;"
            
                "border-radius: 4px;"
                "font-size: 14px;"
            "}"
            "QLineEdit:focus {"
            "    border: 1px solid #07394B;"
            "}"
                        
            
            "QPushButton {background-color: #07394B; color: white; font-size: 18px; border: none; padding: 4px; border-radius: 15px;}      "
            "QPushButton:hover { background-color: #0D4A62 }"
            "QPushButton:pressed { background-color: #052B38 }"
                           
        ")

class LoadIngredient(QFrame):
    def __init__(self, parent=None, ingredient=None):
        super().__init__(parent)
        #self.setStyleSheet("background-color: white ; border-radius: 8px; padding: 4px;")
        #self.modal_widget = GetIngredients(self, mode="edit")
        self.ingredient = ingredient
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        if not self.ingredient:
            return

        date, name, weight, weight_unit, price, price_unit = self.ingredient
        ingredient_btn = QPushButton(f"{name} \n {weight} {weight_unit} - {price} {price_unit}")
        ingredient_btn.setStyleSheet("QPushButton {color: black; font-size: 20px; background-color: white ; border-radius: 8px; padding: 15px;}"
                                     "QPushButton:hover {background-color: #0D4A62;}")
        layout.addWidget(ingredient_btn)
        
        self.setLayout(layout)

        ingredient_btn.clicked.connect(self.show_edit_modal)

    def show_edit_modal(self):
        self.parent().show_modal(mode="edit", ingredient=self.ingredient)
"""
