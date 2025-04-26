from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QGridLayout, QSizePolicy, QHBoxLayout, QStackedWidget, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QScreen
import sys
from MainWidget import MainWidget
from AddRecipeWidget import AddRecipeWidget
from CalculateWidget import CalculateWidget
from Ingredients import IngredientsWidget
from Sales import SalesWidget
from Recipes import RecipesWidget
from AddSalesWidget import AddSalesWidget

class Sidebar(QFrame):
    def __init__(self, main_window):
        super().__init__()

        self.setStyleSheet("background-color: #07394B;")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(240)

        self.main_window = main_window
        self.layout = QVBoxLayout(self) 

        self.create_btns()
        self.active_btn = False

        self.layout.addStretch()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 15, 0, 0)
    
    def create_button(self, text):
        button = QPushButton(text, self)
        button.setFixedHeight(45)
        button.setStyleSheet(
            "QPushButton {background-color: transparent; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 15px;}"
            "QPushButton:hover {background-color: #0D4A62}"
            "QPushButton:pressed {background-color: #052B38}")
        self.layout.addWidget(button)
        return button

    def get_screen_height(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.screen_height = screen_geometry.height()
        return self.screen_height
    
    def create_btns(self):
        self.main_btn = self.create_button("Main")
        self.add_recipe_btn = self.create_button("Add Recipe")
        self.calc_btn = self.create_button("Calculate Recipe")
        self.add_sales_btn = self.create_button("Add Sales")
        self.recipes_btn = self.create_button("Recipes")
        self.ingredient_btn = self.create_button("Ingredients")
        self.sales_btn = self.create_button("Sales")

        self.main_btn.clicked.connect(lambda: self.set_active(self.main_btn, "main"))
        self.add_recipe_btn.clicked.connect(lambda: self.set_active(self.add_recipe_btn, "add_recipe"))
        self.calc_btn.clicked.connect(lambda: self.set_active(self.calc_btn, "calculate"))
        self.add_sales_btn.clicked.connect(lambda: self.set_active(self.add_sales_btn, "add_sales"))
        self.recipes_btn.clicked.connect(lambda: self.set_active(self.recipes_btn, "recipes"))
        self.ingredient_btn.clicked.connect(lambda: self.set_active(self.ingredient_btn, "ingredients"))
        self.sales_btn.clicked.connect(lambda: self.set_active(self.sales_btn, "sales"))

    def set_active(self, btn, name):
        if self.active_btn:
            self.active_btn.setStyleSheet(
            "QPushButton {background-color: transparent; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 15px;}"
            "QPushButton:hover {background-color: #0D4A62}"
            "QPushButton:pressed {background-color: #052B38}")
        
        self.active_btn = btn
        self.active_btn.setStyleSheet(
            "QPushButton {background-color: #0D4A62; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 15px;}")

        self.main_window.switch_window(name)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cake MD")
        self.setStyleSheet("background-color: lightgray;")        

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)    
        main_layout = QHBoxLayout(main_widget)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)

        self.stacked_widget = QStackedWidget(self)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.stacked_widget)

        splitter.setSizes([240, 1000])
        main_layout.addWidget(splitter)

        self.add_all_widgets()

        self.stacked_widget.setCurrentWidget(self.main_page)
        self.sidebar.set_active(self.sidebar.main_btn, "main")

        self.showMaximized()

    def add_all_widgets(self):
        self.add_recipe_window = AddRecipeWidget(self)
        self.stacked_widget.addWidget(self.add_recipe_window)

        self.main_page = MainWidget(self)
        self.stacked_widget.addWidget(self.main_page)

        self.calculate_page = CalculateWidget(self)
        self.stacked_widget.addWidget(self.calculate_page)

        self.ingredients_page = IngredientsWidget(self)
        self.stacked_widget.addWidget(self.ingredients_page)

        self.recipes_page = RecipesWidget(self)
        self.stacked_widget.addWidget(self.recipes_page)

        self.sales_page = SalesWidget(self)
        self.stacked_widget.addWidget(self.sales_page)

        self.add_sales_page = AddSalesWidget(self)
        self.stacked_widget.addWidget(self.add_sales_page)  
        
            
    def switch_window(self, name):
        if name == "add_recipe":
            self.stacked_widget.setCurrentWidget(self.add_recipe_window)
        elif name == "main":
            self.stacked_widget.setCurrentWidget(self.main_page)
        elif name == "calculate":
            self.stacked_widget.setCurrentWidget(self.calculate_page)
        elif name == "ingredients":
            self.stacked_widget.setCurrentWidget(self.ingredients_page)
        elif name == "recipes":
            self.stacked_widget.setCurrentWidget(self.recipes_page)
        elif name == "sales":
            self.stacked_widget.setCurrentWidget(self.sales_page)
        elif name == "add_sales":
            self.stacked_widget.setCurrentWidget(self.add_sales_page)
    

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()