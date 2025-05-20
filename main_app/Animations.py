from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Property
from PySide6.QtGui import QColor

def fade_in_animation(widget, duration=300):
    opacity_effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(opacity_effect)

    fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
    fade_animation.setDuration(duration)
    fade_animation.setStartValue(0)
    fade_animation.setEndValue(1)
    fade_animation.setEasingCurve(QEasingCurve.InOutQuad)  

    fade_animation.start()
    widget._fade_animation = fade_animation  # Keep reference alive so it doesn’t die like your motivation on Monday
    widget.show()

    return fade_animation  # Return the animation object if you need to control it later

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