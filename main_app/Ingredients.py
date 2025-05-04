from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QComboBox, QFrame
from PySide6.QtCore import Qt
from Database import DatabaseManager  # keep this if used elsewhere
from Animations import fade_in_animation  # optional

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

        add_btn.clicked.connect(self.show_modal)

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
        self.setStyleSheet("background-color: lightgray; border-radius: 7px;")
        layout = self.initUI()
        self.setLayout(layout)
        self.adjustSize()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        label = QLabel("Add Ingredients")
        label.setStyleSheet("color: black; font-size: 30px;")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.ing_name, _  = self.create_labeled_input("Ingredient Name:")
        self.ing_weight, self.ing_weight_unit = self.create_labeled_input("Ingredient Weight:", ["g", "kg", "ml", "l", "oz", "lb"])
        self.ing_price, self.ing_price_unit = self.create_labeled_input("Ingredient Price:", ["£", "€", "$"])

        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "QPushButton {background-color: #07394B; color: white; font-size: 14px; border: none; padding: 10px; border-radius: 20px;}"         
            "QPushButton:hover { background-color: #0D4A62 }"
            "QPushButton:pressed { background-color: #052B38 }" )
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(
            "QPushButton {background-color: #07394B; color: white; font-size: 14px; border: none; padding: 10px; border-radius: 20px;}"         
            "QPushButton:hover { background-color: #0D4A62 }"
            "QPushButton:pressed { background-color: #052B38 }" )
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        self.layout.addLayout(buttons_layout)

        self.layout.setSpacing(10)

        return self.layout
    
    def create_labeled_input(self, label_text, combo_items=None):
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        label.setStyleSheet("color: black; font-size: 16px;")
        layout.addWidget(label)

        input_layout = QHBoxLayout()
        line_edit = QLineEdit()
        line_edit.setStyleSheet("background-color: white; color: black;")
        input_layout.addWidget(line_edit)

        combo_box = None
        if combo_items:
            combo_box = QComboBox()
            combo_box.addItems(combo_items)
            combo_box.setStyleSheet("background-color: white; color: black;")
            input_layout.addWidget(combo_box)

        layout.addLayout(input_layout)
        self.layout.addLayout(layout)

        return line_edit, combo_box

    def close_popup(self):
        self.parent().hide_modal()