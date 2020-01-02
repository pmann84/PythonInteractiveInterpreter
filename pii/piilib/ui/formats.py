from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QFont

# ========================================================================
# Widget to contain QTextCharFormats
# ========================================================================


class PiiTextFormats(object):

    def __init__(self):
        self.bold = self.setup_bold_font()
        self.bold_green = self.setup_bold_green_font()
        self.bold_red = self.setup_bold_red_font()
        self.highlight = self.setup_highlight_format()
        self.normal = self.setup_normal_format()

    def setup_normal_format(self):
        normal = QTextCharFormat()
        normal.setFontWeight(QFont.Normal)
        return normal

    def setup_bold_font(self, colour=None):
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        if colour:
            bold_format.setForeground(colour)
        return bold_format

    def setup_bold_green_font(self):
        return self.setup_bold_font(colour=Qt.darkGreen)

    def setup_bold_red_font(self):
        return self.setup_bold_font(colour=Qt.red)

    def setup_highlight_format(self):
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor(Qt.blue).lighter(160))
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
