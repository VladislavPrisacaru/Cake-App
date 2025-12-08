import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from MainUI.Themes.ThemeManager import ThemeManager

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
QQuickStyle.setStyle("Fusion")

# declare classes
theme = ThemeManager()

# expose the classes to the ui
engine.rootContext().setContextProperty("Theme", theme)


engine.load("MainApp/MainUI/Main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())