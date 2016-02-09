import sys
import os
import inspect
from PyQt4 import QtGui

# Fudge the python module
full_script_path = inspect.getfile(inspect.currentframe())
full_source_path = os.path.abspath(os.path.join(full_script_path, "..\\..\\src"))
icon_path = os.path.abspath(os.path.join(full_script_path, "..\\..\\icons\\python.png"))
sys.path.insert(0, full_source_path)

from pii import ui
from pii.ui import dialog

def main():
	app = QtGui.QApplication([])
	icon = QtGui.QIcon(icon_path)
	win = dialog.PiiDialog()
	win.setWindowIcon(icon)
	win.show()
	return app.exec_()

if __name__ == "__main__":
	sys.exit(main())