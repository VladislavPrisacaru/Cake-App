from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QFrame, QMenu, QWidgetAction, QLineEdit, QComboBox, QSizePolicy, QAbstractItemView
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QDoubleValidator
from Database import db
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helper import HelperClass, signals, StickyCombo
from Ingredients.AddIngredients import GetIngredients

class AddRecipeWidget(QWidget):
    def __init__(self, parent=None, ing=None):
        super().__init__()

        self.setObjectName("AddRecipeWidget")

        self._parent = parent
        self.db = db
        
        self.main_layout = QVBoxLayout()
        label = QLabel("Add Recipe")
        label.setObjectName("AddRecipeLabels")
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 50, 0, 0)
        
        container = self.initUI()
        self.main_layout.addWidget(container, alignment=Qt.AlignTop)
        self.main_layout.addStretch()

        self.add_new()

        signals.ingredient_added.connect(self.reload_ingredients)
        signals.ingredient_deleted.connect(self.reload_ingredients)

    def initUI(self):
        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        self.recipe_name, _, self.label = HelperClass.create_labeled_input("Recipe Name:", layout)
        self.label.setObjectName("AddRecipeLabels")
        self.recipe_name.setObjectName("RecipeNameEdit")
        self.recipe_name.setMaxLength(50)

        self.ingredient_box = IngredientBox(self)

        add_ingredient_layout = QHBoxLayout()

        self.add_new_ing = QPushButton("Add New Ingredient")
        self.add_new_ing.setObjectName("AddRecipeBtns")
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
        self.total_price.setObjectName("totallabels")
        self.total_weight.setObjectName("totallabels")
        self.price.setObjectName("totallabels")
        self.weight.setObjectName("totallabels")
        
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

        self.reset_btn.setObjectName("AddRecipeBtns")
        self.save_btn.setObjectName("AddRecipeBtns")

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
        ingredients = [name for _, name, *_ in self.db.get_all_ingredients()]
        
        self.ing_combo = StickyCombo(self)
        self.ing_combo.setObjectName("AddIngredientCombo")
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
        self.overlay.setObjectName("Overlay")
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
        ingredients = [name for _, name, *_ in self.db.get_all_ingredients()]
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

        self.ingredient_box.save_current_recipe()

    def reset_recipe(self):
        self.ingredient_box.delete_all_rows()
        self.recipe_name.setText("")


class IngredientBox(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.db = db
        self.setMinimumSize(200, 500)

        self.setObjectName("IngBoxScroll")
        
        self.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("ContentWidget")
        self.setWidget(self.content_widget)
        
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.addStretch()

    def add_ingredient(self, name):
        # Get data from DB
        try:
            date, ing_name, weight, weight_u, price, price_u = self.db.get_chosen_ingredient(name)
            
            row_widget = QWidget()
            row_widget.setObjectName("RowWidget")
            row_widget.setMaximumHeight(50)
            
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(10, 5, 10, 5)
            row_layout.setSpacing(20)
            
            label = QLabel(ing_name)
            label.setObjectName("IngredientName")
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            row_layout.addWidget(label)
            
            weight_edit = QLineEdit()
            weight_edit.setObjectName("WeightEdit")
            weight_edit.setText(f"{weight}")
            weight_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            validator = QDoubleValidator(0.0, 99999.99, 2)
            validator.setNotation(QDoubleValidator.StandardNotation)
            weight_edit.setValidator(validator)
            row_layout.addWidget(weight_edit)
            weight_edit.textChanged.connect(self.calculate_totals)
            
            weight_combo = QComboBox()
            weight_combo.setObjectName("WeightCombo")
            weight_combo.addItems(["g", "kg", "ml", "l", "oz", "lb"])
            weight_combo.setCurrentText(weight_u)
            weight_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            row_layout.addWidget(weight_combo)
            weight_combo.currentTextChanged.connect(self.calculate_totals)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("DeleteBtn")
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
    
    def delete_all_rows(self):
        for i in reversed(range(self.main_layout.count())):
            row_widget = self.main_layout.itemAt(i).widget()
            if row_widget is not None:
                self.delete_row(row_widget)
    
    def save_current_recipe(self):
        ingredients = []
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

            id = self.db.get_ingredient_id(name)

            ingredient = id, weight, unit

            ingredients.append(ingredient)
        
        self.db.add_recipe(self._parent.recipe_name.text(), ingredients)

        self._parent._parent.manage_recipe_window.load_recipes()


