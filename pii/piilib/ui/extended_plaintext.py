from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QTextCursor

from .formats import PiiTextFormats

# ========================================================================
# Extended Plaintextedit widget
# ========================================================================


class PiiExtendedPlainTextEdit(QPlainTextEdit):
    """
        Provides extended text and document processing
        functionality for the QPlainTextEdit widget
    """
    def __init__(self, parent=None):
        super(PiiExtendedPlainTextEdit, self).__init__(parent)

    def insert_line_break(self, num):
        for i in range(num):
            self.textCursor().insertBlock()
            # self.insertPlainText("\n")

    def insert_tab(self, num):
        for i in range(num):
            self.insertPlainText("\t")

    def text_enter_direction(self, key_pressed):
        if key_pressed == Qt.Key_Backspace:
            return "backward"
        else:
            return "forward"

    def text_enter_module(self):
        text_under = str(self.get_text_under_cursor())
        text_before = str(self.get_text_before_cursor())
        return text_under == "" and text_before == "."

    def text_enter_function(self):
        text_under = str(self.get_text_under_cursor())
        text_before = str(self.get_text_before_cursor())
        return (text_under == "" and text_before == "(") or (text_under == text_before and text_under[0] == "(")

    def text_under_empty(self):
        text_under = str(self.get_text_under_cursor())
        return text_under == ""

    def text_under_eq_text_before(self):
        text_under = str(self.get_text_under_cursor())
        text_before = str(self.get_text_before_cursor())
        return text_under == text_before

    def get_text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return str(tc.selectedText())

    def get_text_before_cursor(self, offset=1):
        tc = self.textCursor()
        for i in range(offset):
            tc.movePosition(QTextCursor.PreviousWord)
        tc.select(QTextCursor.WordUnderCursor)
        return str(tc.selectedText())

    def replace_text_under_cursor(self, replace_text):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        tc.insertText(replace_text)

    def get_text_cursor_position(self, offset=0):
        widget_pos = self.mapToGlobal(self.pos())
        cursor_pos = self.cursorRect().bottomRight()
        offset_pos = QPoint(offset, offset)
        return widget_pos + cursor_pos + offset_pos

    def move_to_line_end(self):
        self.moveCursor(QTextCursor.EndOfLine)

    def move_to_line_start(self, str_prefix=""):
        new_cursor_position = self.textCursor().block().position() + len(str_prefix)
        new_cursor = self.textCursor()
        new_cursor.setPosition(new_cursor_position)
        self.setTextCursor(new_cursor)

    def copy_text_to_clipboard(self, text):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(text, mode=cb.Clipboard)

    def get_clipboard_text(self):
        cb = QApplication.clipboard()
        return cb.text()

    def set_extra_selection_from_cursor(self, cursor):
        # Construct the extra selection
        selection = QTextEdit.ExtraSelection()
        # Set its format to be the highlight format
        selection.format = PiiTextFormats().HIGHLIGHT
        # Set the selections cursor to be the selected
        # word
        selection.cursor = cursor
        # Append the extra selection to the set
        self.setExtraSelections([selection])
        # Copy the text to the clipboard
        selected_text = cursor.selectedText()  # .toAscii().data()
        # print "Copying text [%s] to clipboard" % selected_text
        self.copy_text_to_clipboard(selected_text)

    def clear_extra_selections(self):
        self.setExtraSelections([])

    def paste(self):
        clip_text = self.get_clipboard_text()
        self.insertPlainText(clip_text)
        # print "Pasting...[%s]" % clip_text
