from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QComboBox
from PySide6.QtCore import Qt
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
          
        self.pop_up.setMinimumSize(500, 700)
        layout.addStretch()  
        layout.addWidget(self.pop_up)
        layout.addStretch() 

        self.setLayout(layout)


    def center_widget(self):
        parent_rect = self.parent().rect()
        widget_rect = self.rect()
        x = parent_rect.x() + (parent_rect.width() - widget_rect.width()) // 2
        y = parent_rect.y() + (parent_rect.height() - widget_rect.height()) // 2
        self.move(x, y)


class GetIngredients(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: lightgray; border-radius: 7px;")
        main_widget = QWidget(self)
        layout = self.initUI()
        main_widget.setLayout(layout)

    def initUI(self):
        self.layout = QVBoxLayout()

        label = QLabel("Add Ingredients")
        label.setStyleSheet("color: black; font-size: 30px;")
        label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout.addWidget(label)

        ing_name_label = QLabel("Ingredient Name:")
        ing_name_label.setStyleSheet("color: black; font-size: 16px;")
        self.layout.addWidget(ing_name_label)

        ing_name_line = QLineEdit()
        ing_name_line.setStyleSheet("background-color: white; color: black;")
        self.layout.addWidget(ing_name_line)

        h_layout_1 = QHBoxLayout()
        ing_type_label = QLabel("Ingredient Weight:")
        ing_type_label.setStyleSheet("color: black; font-size: 16px;")
        h_layout_1.addWidget(ing_type_label)
        
        ing_type_combo = QComboBox()
        ing_type_combo.addItems(["g", "kg", "l", "lb", "oz"])
        ing_type_combo.setStyleSheet("background-color: white; color: black;")
        h_layout_1.addWidget(ing_type_combo)
        self.layout.addLayout(h_layout_1)

        h_layout_2 = QHBoxLayout()
        ing_price_label = QLabel("Ingredient Price:")
        ing_price_label.setStyleSheet("color: black; font-size: 16px;")
        h_layout_2.addWidget(ing_price_label)

        ing_price_combo = QComboBox()
        ing_price_combo.addItems([ "£", "€", "$"])
        ing_price_combo.setStyleSheet("background-color: white; color: black;")
        h_layout_2.addWidget(ing_price_combo)
        self.layout.addLayout(h_layout_2)

        save_btn2 = QPushButton("Save")
        save_btn2.setStyleSheet("background-color: white; color: black;")
        save_btn2.clicked.connect(self.close_popup)
        self.layout.addWidget(save_btn2)

        self.layout.addStretch()
        self.layout.setSpacing(20)

        return self.layout

    def close_popup(self):
        self.parent().close()