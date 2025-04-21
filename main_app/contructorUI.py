from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QScreen
import sys

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #07394B;")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(240)
        self.setMinimumHeight(self.get_screen_height())
        self.setMaximumHeight(self.get_screen_height())

        self.layout = QVBoxLayout(self) 

        self.create_button("Main")
        self.create_button("Add Recipe")
        self.create_button("Calculate Recipe")
        self.create_button("Add Sales")
        self.create_button("Recipes")
        self.create_button("Ingredients")
        self.create_button("Sales")

        self.layout.addStretch()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 15, 0, 0)
    
    def create_button(self, text):
        button = QPushButton(text, self)
        button.setFixedHeight(45)
        button.setStyleSheet("QPushButton {background-color: transparent; font-weight: bold; color: white; font-size: 16px; border: none; text-align: left; padding-left: 15px;}"
                             "QPushButton:hover {background-color: #0D4A62}"
                             "QPushButton:pressed {background-color: #052B38}")
        self.layout.addWidget(button)

    def get_screen_height(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.screen_height = screen_geometry.height()
        return self.screen_height


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cake MD")
        self.setStyleSheet("background-color: lightgray;")        

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)    

        self.sidebar = Sidebar()
        self.sidebar.setParent(self)
        self.showMaximized()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()