from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QComboBox, QFrame, QGridLayout
from PySide6.QtCore import Qt, QRegularExpression, QEasingCurve, QPropertyAnimation, Property, QObject, Signal, QEvent
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator, QColor


class HelperClass:
    @staticmethod
    def create_labeled_input(label_text, main_layout, combo_items=None, place_holder_text=None): # to create the input fields label / line edit / combobox
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        layout.addWidget(label)

        input_layout = QHBoxLayout()
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(place_holder_text)
        line_edit.setMaxLength(30)

        # set validation
        if "Name" in label_text:
            regex = QRegularExpression("[a-zA-Z0-9 ]*")
            validator = QRegularExpressionValidator(regex)
            line_edit.setValidator(validator)
        elif label_text == "Ingredient Weight:" or label_text == "Ingredient Price:":
            validator = QDoubleValidator(0.0, 99999.99, 2)
            validator.setNotation(QDoubleValidator.StandardNotation)
            line_edit.setValidator(validator)

        line_edit.setStyleSheet("background-color: white; color: black;")
        input_layout.addWidget(line_edit)

        combo_box = None
        if combo_items:
            combo_box = QComboBox()
            combo_box.addItems(combo_items)
            combo_box.setStyleSheet("background-color: white; color: black; font-size: 15px;")
            input_layout.addWidget(combo_box)

        layout.addLayout(input_layout)
        main_layout.addLayout(layout)

        return line_edit, combo_box, label
    
    class AnimatedLabel(QLabel):
        def __init__(self, start_bg, end_bg, start_text, end_text, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._bg_color = QColor(*start_bg)
            self._text_color = QColor(*start_text)

            self.start_bg = QColor(*start_bg)
            self.end_bg = QColor(*end_bg)

            self.start_text = QColor(*start_text)
            self.end_text = QColor(*end_text)

            self._bg_anim = QPropertyAnimation(self, b"bg_color")
            self._bg_anim.setDuration(300)
            self._bg_anim.setEasingCurve(QEasingCurve.OutQuad)

            self._text_anim = QPropertyAnimation(self, b"text_color")
            self._text_anim.setDuration(300)
            self._text_anim.setEasingCurve(QEasingCurve.OutQuad)

            self.update_stylesheet()

        def enterEvent(self, event):
            self._bg_anim.stop()
            self._text_anim.stop()

            self._bg_anim.setStartValue(self._bg_color)
            self._bg_anim.setEndValue(self.end_bg)

            self._text_anim.setStartValue(self._text_color)
            self._text_anim.setEndValue(self.end_text)

            self._bg_anim.start()
            self._text_anim.start()

            super().enterEvent(event)

        def leaveEvent(self, event):
            self._bg_anim.stop()
            self._text_anim.stop()

            self._bg_anim.setStartValue(self._bg_color)
            self._bg_anim.setEndValue(self.start_bg)

            self._text_anim.setStartValue(self._text_color)
            self._text_anim.setEndValue(self.start_text)

            self._bg_anim.start()
            self._text_anim.start()

            super().leaveEvent(event)

        def get_bg_color(self):
            return self._bg_color

        def set_bg_color(self, color):
            self._bg_color = color
            self.update_stylesheet()

        def get_text_color(self):
            return self._text_color

        def set_text_color(self, color):
            self._text_color = color
            self.update_stylesheet()

        def update_stylesheet(self):
            self.setStyleSheet(
                f"""
                QLabel {{
                    font-size: 20px;
                    background-color: rgba({self._bg_color.red()}, {self._bg_color.green()}, {self._bg_color.blue()}, {self._bg_color.alpha()});
                    color: rgba({self._text_color.red()}, {self._text_color.green()}, {self._text_color.blue()}, {self._text_color.alpha()});
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                    border: 0px solid black;
                }}
                """
            )

        bg_color = Property(QColor, get_bg_color, set_bg_color)
        text_color = Property(QColor, get_text_color, set_text_color)

class Signals(QObject):
    ingredient_added = Signal()
    ingredient_deleted = Signal()

signals = Signals()


class StickyCombo(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.view().viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                if index.isValid():
                    # Emit current text but DO NOT close popup
                    self.setCurrentIndex(index.row())
                    self.activated.emit(index.row())
                return True  # block the default behavior (closing)
        return super().eventFilter(obj, event)
    
    def mousePressEvent(self, e):
        self.showPopup()
        super().mousePressEvent(e)