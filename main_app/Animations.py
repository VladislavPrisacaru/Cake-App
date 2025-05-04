from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import QEasingCurve, QPropertyAnimation

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