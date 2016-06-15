from PyQt4 import QtGui, QtCore

# ========================================================================
# Python Autocompleter
# ========================================================================


class PiiAutoCompleter(QtGui.QCompleter):
    # Define a signal here that gets emitted when a user
    # hits enter or selects a word, then on the text edit
    # connect a function to that signal that replaces the
    # current word with the new one!
    def __init__(self, matches, widget=None, font=None, on_completion=None):
        super(PiiAutoCompleter, self).__init__(matches)
        # Connect the activated signal to the input function
        if on_completion:
            self.activated.connect(on_completion)
        # If we have been given a widget set it
        if widget:
            self.setWidget(widget)
        # Now set the font if its been passed
        if font:
            self.set_font(font)
        # Set some of the properties of the completer
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # Store the matches as a set
        self.all_matches = set(matches)

    def update_matches(self, matches):
        self.all_matches = set(matches)
        new_matches = list(self.all_matches)
        new_matches.sort()
        model = QtGui.QStringListModel(new_matches, self)
        self.setModel(model)

    # def update_completion_prefix(self, prefix):
    #     if completion_prefix != self.completionPrefix():
    #         if completion_prefix.strip() != '':
    #             self.complete()

    def set_font(self, font):
        self.popup().setFont(font)

    def is_visible(self):
        return self.popup().isVisible()

    def hide(self):
        self.popup().hide()

    def hide_if_visible(self):
        if self.is_visible():
            self.hide()

    @property
    def matches_exist(self):
        return bool(self.all_matches)