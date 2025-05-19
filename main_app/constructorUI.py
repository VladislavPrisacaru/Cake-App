from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
    QFrame, QSizePolicy, QHBoxLayout, QStackedWidget, QLabel)
import sys
from Animations import fade_in_animation
from Database import DatabaseManager
from Main.MainWidget import MainWidget
from Recipes.AddRecipe import AddRecipeWidget
from Recipes.ManageRecipes import ManageRecipesWidget
from Ingredients.AddIngredients import AddIngredientsWidget
from Ingredients.ManageIngredients import ManageIngredientsWidget
from Sales.AddSales import AddSalesWidget
from Sales.ManageSales import ManageSalesWidget
from Stock.AddStock import AddStockWidget
from Stock.ManageStock import ManageStockWidget
from Options import OptionsWidget

db = DatabaseManager("cakeshop.db")

class Sidebar(QFrame):
    def __init__(self, main_window):
        super().__init__()

        self.setStyleSheet("background-color: #07394B;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMinimumWidth(240)

        self.main_window = main_window # Reference to the main window class
        self.layout = QVBoxLayout(self)

        self.create_btns()
        self.active_btn = False

        self.layout.addStretch()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 15, 0, 0)

    def create_button(self, text): # to create loads of buttons easy
        button = QPushButton(text, self)
        button.setFixedHeight(45)
        button.setStyleSheet(
            "QPushButton {background-color: transparent; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 35px;}"
            "QPushButton:hover {background-color: #0D4A62}"
            "QPushButton:pressed {background-color: #052B38}")
        self.layout.addWidget(button)
        return button

    def create_header(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: white; font-size: 18px; border: none; text-align: left; padding-left: 10px;")
        self.layout.addWidget(label)

    def create_btns(self): # the menu buttons and its connections
        self.main_btn = self.create_button("Main")
        self.main_btn.clicked.connect(lambda: self.set_active(self.main_btn, "main"))

        # --- Recipes ---
        self.create_header("Recipes")
        self.add_recipe_btn = self.create_button("Add Recipe")
        self.manage_recipe_btn = self.create_button("Manage Recipes")

        self.add_recipe_btn.clicked.connect(lambda: self.set_active(self.add_recipe_btn, "add_recipe"))
        self.manage_recipe_btn.clicked.connect(lambda: self.set_active(self.manage_recipe_btn, "manage_recipes"))

        # --- Ingredients ---
        self.create_header("Ingredients")
        self.add_ingredient_btn = self.create_button("Add Ingredients")
        self.manage_ingredient_btn = self.create_button("Manage Ingredients")

        self.add_ingredient_btn.clicked.connect(lambda: self.set_active(self.add_ingredient_btn, "add_ingredients"))
        self.manage_ingredient_btn.clicked.connect(lambda: self.set_active(self.manage_ingredient_btn, "manage_ingredients"))

        # --- Sales ---
        self.create_header("Sales")
        self.add_sales_btn = self.create_button("Add Sales")
        self.manage_sales_btn = self.create_button("Manage Sales")

        self.add_sales_btn.clicked.connect(lambda: self.set_active(self.add_sales_btn, "add_sales"))
        self.manage_sales_btn.clicked.connect(lambda: self.set_active(self.manage_sales_btn, "manage_sales"))

        # --- Stock ---
        self.create_header("Stock")
        self.add_stock_btn = self.create_button("Add Stock")
        self.manage_stock_btn = self.create_button("Manage Stock")

        self.add_stock_btn.clicked.connect(lambda: self.set_active(self.add_stock_btn, "add_stock"))
        self.manage_stock_btn.clicked.connect(lambda: self.set_active(self.manage_stock_btn, "manage_stock"))

        # --- Options ---
        self.options_btn = self.create_button("Options")
        self.options_btn.clicked.connect(lambda: self.set_active(self.options_btn, "options"))

    def set_active(self, btn, name): # keep the active button highlighted and switch the window
        if self.active_btn:
            self.active_btn.setStyleSheet(
                "QPushButton {background-color: transparent; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 35px;}"
                "QPushButton:hover {background-color: #0D4A62}"
                "QPushButton:pressed {background-color: #052B38}")

        self.active_btn = btn
        self.active_btn_name = name
        self.active_btn.setStyleSheet(
            "QPushButton {background-color: #0D4A62; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 35px;}")

        self.main_window.switch_window(name)


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.setWindowTitle("Cake MD")
        self.setStyleSheet("background-color: lightgray;")
        self.db = db
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.stacked_widget = QStackedWidget(self) # to store all the pages

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        self.add_all_widgets()

        self.stacked_widget.setCurrentWidget(self.main_page)
        self.sidebar.set_active(self.sidebar.main_btn, "main")

        self.showMaximized()

    def add_all_widgets(self):
        self.main_page = MainWidget(self)
        self.stacked_widget.addWidget(self.main_page)

        # --- Recipes
        self.add_recipe_window = AddRecipeWidget(self)
        self.stacked_widget.addWidget(self.add_recipe_window)

        self.manage_recipe_window = ManageRecipesWidget(self)
        self.stacked_widget.addWidget(self.manage_recipe_window)

        # --- Ingredients
        self.add_ingredients_window = AddIngredientsWidget(self)
        self.stacked_widget.addWidget(self.add_ingredients_window)

        self.manage_ingredients_window = ManageIngredientsWidget(self)
        self.stacked_widget.addWidget(self.manage_ingredients_window)

        # --- Sales
        self.add_sales_window = AddSalesWidget(self)
        self.stacked_widget.addWidget(self.add_sales_window)

        self.manage_sales_window = ManageSalesWidget(self)
        self.stacked_widget.addWidget(self.manage_sales_window)

        # --- Stock
        self.add_stock_window = AddStockWidget(self)
        self.stacked_widget.addWidget(self.add_stock_window)

        self.manage_stock_window = ManageStockWidget(self)
        self.stacked_widget.addWidget(self.manage_stock_window)

        # --- Options
        self.options_page = OptionsWidget(self)
        self.stacked_widget.addWidget(self.options_page)

    def switch_window(self, name):
        widget_map = {
            "main": self.main_page,

            "add_recipe": self.add_recipe_window,
            "manage_recipes": self.manage_recipe_window,

            "add_ingredients": self.add_ingredients_window,
            "manage_ingredients": self.manage_ingredients_window,

            "add_sales": self.add_sales_window,
            "manage_sales": self.manage_sales_window,

            "add_stock": self.add_stock_window,
            "manage_stock": self.manage_stock_window,

            "options": self.options_page
        }

        widget = widget_map.get(name)

        if self.stacked_widget.currentWidget() == widget:
            return

        fade_in_animation(widget)
        self.stacked_widget.setCurrentWidget(widget)
    
    def closeEvent(self, event):
        self.db.close_conn()
        event.accept()


app = QApplication(sys.argv)
window = MainWindow(db)
window.show()
app.exec()