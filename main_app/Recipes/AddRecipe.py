from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QFrame, QMenu, QWidgetAction, QLineEdit, QComboBox, QSizePolicy, QAbstractItemView
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QDoubleValidator
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helper import HelperClass, signals, StickyCombo
from Ingredients.AddIngredients import GetIngredients

class AddRecipeWidget(QWidget):
    def __init__(self, parent=None, ing=None):
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

        self.add_new()
        self.set_style()

        signals.ingredient_added.connect(self.reload_ingredients)
        signals.ingredient_deleted.connect(self.reload_ingredients)

    def initUI(self):
        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        self.recipe_name, _, self.label = HelperClass.create_labeled_input("Recipe Name:", layout)
        self.recipe_name.setMaxLength(50)

        self.ingredient_box = IngredientBox(self)

        add_ingredient_layout = QHBoxLayout()

        self.add_new_ing = QPushButton("Add New Ingredient")
        self.add_existing = self.existing_ingredients_combo()

        add_ingredient_layout.addWidget(self.add_new_ing)
        add_ingredient_layout.addWidget(self.add_existing)

        self.add_new_ing.clicked.connect(lambda: self.show_modal("add"))

        add_ingredient_layout.setSpacing(100)
        add_ingredient_layout.setContentsMargins(50, 20, 50, 20)

        layout.addLayout(add_ingredient_layout)

        layout.addWidget(self.ingredient_box)


        totals_layout = QHBoxLayout()
        self.total_price = QLabel("Total Price:")
        self.price = QLabel("0")
        self.total_weight = QLabel("Raw Weight:")
        self.weight = QLabel("0")
        self.total_price.setObjectName("totallabel")
        self.total_weight.setObjectName("totallabel")
        self.price.setObjectName("totallabel")
        self.weight.setObjectName("totallabel")
        
        totals_layout.addWidget(self.total_price)
        totals_layout.addWidget(self.price)
        totals_layout.addStretch()
        totals_layout.addWidget(self.total_weight)
        totals_layout.addWidget(self.weight)
        totals_layout.setContentsMargins(40,8,40,0)

        layout.addLayout(totals_layout)


        reset_save_layout = QHBoxLayout()

        self.reset_btn = QPushButton("Reset Recipe")
        self.save_btn = QPushButton("Save Recipe")

        reset_save_layout.addWidget(self.reset_btn)
        reset_save_layout.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self.save_recipe)
        self.reset_btn.clicked.connect(self.reset_recipe)

        reset_save_layout.setSpacing(100)
        reset_save_layout.setContentsMargins(50, 20, 50, 20)

        layout.addLayout(reset_save_layout)

        layout.setContentsMargins(200, 0, 200, 0)
        return main_container
    
    def existing_ingredients_combo(self):
        ingredients = [name for _, name, *_ in self._parent.db.get_all_ingredients()]
        
        self.ing_combo = StickyCombo(self)
        self.ing_combo.addItems(ingredients)
        self.ing_combo.setMaxVisibleItems(10)
        self.ing_combo.setCurrentText("Add Existing Ingredient")

        popup = self.ing_combo.view()
        popup.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.ing_combo.currentTextChanged.connect(self.handle_combo_selection)

        return self.ing_combo

    def handle_combo_selection(self, name):
        if name and name != "Add Existing Ingredient":
            self.ingredient_box.add_ingredient(name)
            self.ing_combo.blockSignals(True)
            self.ing_combo.setCurrentText("Add Existing Ingredient")
            self.ing_combo.blockSignals(False)
    
    def add_new(self):
        self.overlay = QWidget(self) # create an overlay widget
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.overlay.hide()
        
        self.modal_widget = GetIngredients(parent=self)
        self.modal_widget.hide()

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

    def reload_ingredients(self):
        ingredients = [name for _, name, *_ in self._parent.db.get_all_ingredients()]
        self.ing_combo.blockSignals(True)
        self.ing_combo.clear()
        self.ing_combo.addItems(ingredients)
        self.ing_combo.setCurrentText("Add Existing Ingredient")
        self.ing_combo.blockSignals(False)
    
    def load_ingredients(self):
        self._parent.add_ingredients_window.load_ingredients()
        last_ing = self.db.get_last_ingredient()
        self.ingredient_box.add_ingredient(last_ing)
    
    def save_recipe(self):
        pass

    def reset_recipe(self):
        pass

    def set_style(self):
        self.setStyleSheet("""
            QLabel {
                color: black; 
                font-size: 25px;}
            
            QLabel#totallabel {
                color: black; 
                font-size: 32px; 
                padding: 6px;}
                           
            QLineEdit {
                padding: 2px;
                border-radius: 4px;
                font-size: 22px;}
                           
            QLineEdit:focus {
                border: 1px solid #07394B;}
            
            QPushButton {background-color: #07394B; color: white; font-size: 22px; border: none; padding: 7px; border-radius: 15px;}
            QPushButton:hover {background-color: #0D4A62}
            QPushButton:pressed {background-color: #052B38}

            QComboBox {
                background-color: #07394B;
                color: white;
                font-size: 22px;
                border: none;
                padding: 7px;
                border-radius: 15px;
            }

            QComboBox:hover {
                background-color: #0D4A62;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 20px;
                height: 20px;
                image: url(Recipes/white_arrow.png);
                border: none;
                padding-right: 8px;
            }

            QComboBox QAbstractItemView {
                background-color: #07394B;
                color: white;
                selection-background-color: #0D4A62;
                border-radius: 10px;
                font-size: 20px;
                padding: 5px;
            }        

            QComboBox QAbstractItemView QScrollBar:vertical {
                background: #07394B;
                width: 12px;
                margin: 0px;
                border-radius: 10px;}   

            QComboBox QAbstractItemView QScrollBar::handle:vertical {
                background: #0D4A62; 
                min-height: 20px;
                border-radius: 8px;}
                           
            QComboBox QAbstractItemView QScrollBar::add-page:vertical,
            QComboBox QAbstractItemView QScrollBar::sub-page:vertical {
                height: 0px;
                subcontrol-origin: margin;
                subcontrol-position: top;  /* for add-line */
                background: none;
                border: none;
            }
                           
            QComboBox QAbstractItemView::up-button, 
            QComboBox QAbstractItemView::down-button {
                /* Hide the scrollbar buttons completely */
                width: 0px;
                height: 0px;}
            """)

class IngredientBox(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.db = parent.db
        self.setMinimumSize(200, 500)
        
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
        try:
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
            validator = QDoubleValidator(0.0, 99999.99, 2)
            validator.setNotation(QDoubleValidator.StandardNotation)
            weight_edit.setValidator(validator)
            row_layout.addWidget(weight_edit)
            weight_edit.textChanged.connect(self.calculate_totals)
            
            weight_combo = QComboBox()
            weight_combo.addItems(["g", "kg", "ml", "l", "oz", "lb"])
            weight_combo.setCurrentText(weight_u)
            weight_combo.setStyleSheet("background-color: white; color: black; font-size: 18px;")
            weight_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            row_layout.addWidget(weight_combo)
            weight_combo.currentTextChanged.connect(self.calculate_totals)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("deleteBtn")
            delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            row_layout.addWidget(delete_btn)

            delete_btn.clicked.connect(lambda checked, r=row_widget: self.delete_row(r))

            self.main_layout.insertWidget(0, row_widget)

            self.calculate_totals()
            #self._parent.add_existing.setCurrentText("Add Existing Ingredient")
        except:
            pass

    def calculate_totals(self):
        current_price = 0
        current_weight = 0

        for i in range(self.main_layout.count()):
            row_widget = self.main_layout.itemAt(i).widget()
            if row_widget is None:
                continue 

            name_lbl = row_widget.findChild(QLabel)
            weight_edit = row_widget.findChild(QLineEdit)
            unit_combo = row_widget.findChild(QComboBox)

            name = name_lbl.text()
            weight = float(weight_edit.text())
            unit = unit_combo.currentText()

            weight = self.weight_to_grams(weight, unit)
            
            _, _, db_weight, db_weight_unit, db_price, db_price_unit = self.db.get_chosen_ingredient(name)

            db_weight = self.weight_to_grams(db_weight, db_weight_unit)
            
            price_per_gram = db_price / db_weight
            price_per_ingredient = price_per_gram * weight
            current_price += price_per_ingredient
            current_weight += weight

        self._parent.price.setText(f"{current_price:.2f}")
        self._parent.weight.setText(f"{current_weight}")
    
    def weight_to_grams(self, weight, unit):
        conversions = {
            "kg": 1000,
            "l": 1000,
            "ml": 1,
            "g": 1,
            "oz": 28.3495,
            "lb": 453.592
        }

        return weight * conversions.get(unit, 1)
        
    def delete_row(self, row):
        self.main_layout.removeWidget(row)
        row.setParent(None)
        row.deleteLater()
        self.calculate_totals()
    
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
                border: 1px solid #07394B;
            }
        """
        self.setStyleSheet(style)