#!python3

import sys
import os
import inspect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# Construct a path to the icon
full_script_path = inspect.getfile(inspect.currentframe())
icon_path = os.path.abspath(os.path.join(full_script_path, "..\\..\\icons\\python.png"))

from piilib.ui.dialog import PiiDialog


def main():
    global app
    app = QApplication([])
    icon = QIcon(icon_path)
    win = PiiDialog()
    win.setWindowIcon(icon)
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
