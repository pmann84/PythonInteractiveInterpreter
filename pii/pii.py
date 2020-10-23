#!python3

import sys
import os
import inspect
import resource_rc
from enum import Enum
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# Construct a path to the icon
full_script_path = inspect.getfile(inspect.currentframe())
icon_path = os.path.abspath(os.path.join(full_script_path, "..\\..\\icons\\python.png"))

from piilib.ui.dialog import PiiDialog


class Theme(Enum):
    Dark = 1
    Light = 2


def set_stylesheet(app, theme = Theme.Dark):
    theme = "dark" if theme == Theme.Dark else "light"
    theme_rc_path = f":/{theme}.qss"
    file = QFile(theme_rc_path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())


def main():
    global app
    app = QApplication([])
    set_stylesheet(app)
    icon = QIcon(icon_path)
    win = PiiDialog()
    win.setWindowIcon(icon)
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
