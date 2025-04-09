from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #333;")
        self.setMaximumWidth(250)
        self.setMinimumWidth(0)

        self.layout = QVBoxLayout(self) 

        self.create_button("Main")
        self.create_button("Ingredient Managment")
        self.create_button("Sales Managment")
        self.create_button("Recipe Managment")

        self.setLayout(self.layout)
    
    def create_button(self, text):
        button = QPushButton(text, self)
        button.setFixedHeight(50)
        button.setFont(QFont("Arial", 11))
        self.layout.addWidget(button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cake MD")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.hamburger_button = QPushButton(self)
        self.hamburger_button.setText("☰")
        self.hamburger_button.setStyleSheet("font-size: 25px;")
        self.hamburger_button.clicked.connect(self.toggle_sidebar)
        self.hamburger_button.move(10,10)

        #layout.addWidget(self.hamburger_button)

        self.sidebar = Sidebar()
        self.sidebar.setParent(self)
        self.sidebar.move(0,20)

        self.sidebar.setMaximumWidth(0)
        self.sidebar.setMinimumWidth(0)

        self.sidebar_open = False

        self.hamburger_button.raise_()

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar.setMinimumWidth(0)
            self.sidebar.setMaximumWidth(0)
        else:
            self.sidebar.setMinimumWidth(190)
            self.sidebar.setMaximumWidth(150)
            self.sidebar.setMinimumHeight(300)
            self.sidebar.setMaximumHeight(300)

        if self.sidebar_open:
            self.hamburger_button.setText("☰")
        else:
            self.hamburger_button.setText("✖")
        
        self.sidebar_open = not self.sidebar_open


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()