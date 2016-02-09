from PyQt4 import QtGui, QtCore

#========================================================================
# Widget to contain QTextCharFormats
#========================================================================

class PiiTextFormats(object):

	def __init__(self):
		self.bold = self.setup_bold_font()
		self.bold_green = self.setup_bold_green_font()
		self.bold_red = self.setup_bold_red_font()
		self.highlight = self.setup_highlight_format()
		self.normal = self.setup_normal_format()

	def setup_normal_format(self):
		normal = QtGui.QTextCharFormat()
		normal.setFontWeight(QtGui.QFont.Normal)
		return normal

	def setup_bold_font(self, colour=None):
		bold_format = QtGui.QTextCharFormat()
		bold_format.setFontWeight(QtGui.QFont.Bold)
		if colour:
			bold_format.setForeground(colour)
		return bold_format

	def setup_bold_green_font(self):
		return self.setup_bold_font(colour=QtCore.Qt.green)

	def setup_bold_red_font(self):
		return self.setup_bold_font(colour=QtCore.Qt.red)

	def setup_highlight_format(self):
		highlight_format = QtGui.QTextCharFormat()
		highlight_format.setBackground(QtGui.QColor(QtCore.Qt.blue).lighter(160))
		return highlight_format

	@property
	def NORMAL(self):
		return self.normal

	@property
	def BOLD(self):
		return self.bold

	@property
	def BOLD_GREEN(self):
		return self.bold_green

	@property
	def BOLD_RED(self):
		return self.bold_red

	@property
	def HIGHLIGHT(self):
		return self.highlight