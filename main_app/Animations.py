from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation

def fade_in_animation(widget):
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
        fade_animation.setDuration(300)
        fade_animation.setStartValue(0)
        fade_animation.setEndValue(1)
        fade_animation.setEasingCurve(QEasingCurve(QEasingCurve.Type.InOutQuad))

        fade_animation.start()
        widget._fade_animation = fade_animation  # Keep reference alive

        widget.show()