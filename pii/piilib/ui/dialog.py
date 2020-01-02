from PyQt5.QtWidgets import QDialog, QVBoxLayout

# Local Imports
from .terminal import PiiTerminal

# ========================================================================
# Python Dialog Widget
# ========================================================================


class PiiDialog(QDialog):

    def __init__(self):
        super(PiiDialog, self).__init__()
        self.resize(700, 400)
        self.setWindowTitle("Pii")
        self.setLayout(QVBoxLayout())
        layout_margin = 1.0
        self.layout().setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)
        self.pii_term = PiiTerminal()
        self.layout().addWidget(self.pii_term)
