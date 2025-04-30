from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFrame, QLabel,
    QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QScreen
from Database import DatabaseManager  # keep this if used elsewhere
from Animations import fade_in_animation  # optional

class IngredientsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.add_btn()

    def add_btn(self):
        layout = QHBoxLayout()

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

        add_btn.clicked.connect(self.set_ingredient_info)

    def set_ingredient_info(self):
        self.modal_widget = ModalWidget(self)
        self.modal_widget.raise_()  # Ensure the modal is on top
        self.modal_widget.show()
        # fade_in_animation(self.modal_widget)


class ModalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(parent.rect())

        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 70);")
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.show()

        self.setAttribute(Qt.WA_DeleteOnClose)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.pop_up = GetIngredients(self)
        self.pop_up.setFixedSize(300, 200)
        layout.addWidget(self.pop_up)

        self.setLayout(layout)


class GetIngredients(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: lightgray; border-radius: 7px;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        label = QLabel("Ingredients List")
        label.setStyleSheet("color: black; font-size: 18px;")
        layout.addWidget(label)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("color: black;")
        save_btn.clicked.connect(self.close_popup)
        layout.addWidget(save_btn)

    def close_popup(self):
        self.parent().close()