import sys
import os
import inspect
from PyQt4 import QtGui

# Construct a path to the icon
full_script_path = inspect.getfile(inspect.currentframe())
icon_path = os.path.abspath(os.path.join(full_script_path, "..\\..\\icons\\python.png"))

import piilib


def main():
    app = QtGui.QApplication([])
    icon = QtGui.QIcon(icon_path)
    win = piilib.ui.dialog.PiiDialog()
    win.setWindowIcon(icon)
    win.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
