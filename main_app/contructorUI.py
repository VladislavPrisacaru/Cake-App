from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QGridLayout, QSizePolicy, QHBoxLayout, QStackedWidget, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QScreen
import sys

class Sidebar(QFrame):
    def __init__(self, main_window):
        super().__init__()

        self.setStyleSheet("background-color: #07394B;")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(240)
        self.setMinimumHeight(self.get_screen_height())
        self.setMaximumHeight(self.get_screen_height())

        self.main_window = main_window
        self.layout = QVBoxLayout(self) 

        self.create_btns()

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

        self.main_btn.clicked.connect(lambda: self.main_window.switch_window("main"))
        self.add_recipe_btn.clicked.connect(lambda: self.main_window.switch_window("add_recipe"))


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

        self.showMaximized()

    def create_addrecipe_window(self):
        self.add_recipe_window = QWidget(self)
        layout = QVBoxLayout()
        self.add_recipe_window.setLayout(layout)

        button = QPushButton("Hi")
        layout.addWidget(button)
        self.stacked_widget.addWidget(self.add_recipe_window)

    def create_main_window(self):
        self.main_page = QWidget(self)
        self.main_page.setLayout(QVBoxLayout())
        self.main_page.layout().addWidget(QLabel("Welcome to Cake MD!"))
        self.stacked_widget.addWidget(self.main_page)
            
    def switch_window(self, name):
        if name == "add_recipe":
            self.create_addrecipe_window()
            self.stacked_widget.setCurrentWidget(self.add_recipe_window)
        elif name == "main":
            self.create_main_window()
            self.stacked_widget.setCurrentWidget(self.main_page)
    

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()