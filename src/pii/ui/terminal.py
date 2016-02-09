from PyQt4 import QtGui, QtCore
import sys
from contextlib import contextmanager

# Local imports 
from .. import history
from .. import interpreter
from ..interpreter import redirect_stdout_and_stderr
from .. import completer
from .extended_plaintext import PiiExtendedPlainTextEdit
from .formats import PiiTextFormats

#========================================================================
# Python Terminal Widget
#========================================================================

class PiiTerminal(PiiExtendedPlainTextEdit):

	#========================================================================
	# Global Class settings
	#========================================================================

	WELCOME_FORMAT_DICT = 	{ 
								"version_info": sys.version, 
								"platform": sys.platform 
							}
	WELCOME = "Welcome to PII - Python Interactive Interpreter\nRunning Python {version_info} on {platform}\n\n".format(**WELCOME_FORMAT_DICT)
	PS1 = ">>> "
	PS2 = "..> "
	RESULT_PROMPT = "Result "
	TAB_WIDTH = 4
	FONT_SIZE = 9
	IGNORE_KEYS = [QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]

	#========================================================================
	# Class constructor
	#========================================================================

	def __init__(self):
		super(PiiTerminal, self).__init__()
		self.user_prompt = self.PS1
		self.is_multiline = False
		self.setLineWrapMode(QtGui.QPlainTextEdit.WidgetWidth)
		# Set up the font
		self.font_point_size = self.FONT_SIZE
		self.setup_text_edit_font()
		self.setFont(self.text_editor_font)
		# Set the tab width
		self.setTabStopWidth(self.TAB_WIDTH*self.font_point_size*1.5)
		# Setup the command history
		self.command_history = history.PiiCommandHistory()
		# Setup the process
		self.pii_interpreter = None
		self.initialise_interpreter()
		# Setup a completer
		self.pii_completer = self.get_completer([])
		# Print first text on the terminal
		# welcome and initial prompt
		self.insertPlainText(self.WELCOME)
		self.write_user_prompt(format=PiiTextFormats().BOLD_RED)
		# Setup some extra variables for sorting out
		# mouse behaviour
		self.has_just_double_clicked = False
		self.has_just_selected = False

	#========================================================================
	# Overriden methods of baseclass or system methods
	#========================================================================

	# Any class that has a write method can have stdout
	# redirected to it!
	def write(self, txt):
		self.insertPlainText(txt)

	# Here we sort out all the mouse events and 
	# determine appropriate behaviour for the 
	# terminal
	def contextMenuEvent(self, event):
		pass

	def mousePressEvent(self, event):
		self.old_cursor_pos = self.cursorForPosition(event.pos())

	def mouseReleaseEvent(self, event):
		# If the middle mouse was pressed then paste in the text
		if not self.has_just_double_clicked and event.button() == QtCore.Qt.MidButton:
			# Reset the extra selections of the text edit
			self.clear_extra_selections()
			# Paste the contents of the clipboard
			# into the text edit
			self.paste()
		elif not self.has_just_double_clicked and not self.has_just_selected:
			cursor = self.cursorForPosition(event.pos())
			self.set_extra_selection_from_cursor(cursor)
		else:
			self.has_just_double_clicked = False
			self.has_just_selected = False

	def mouseDoubleClickEvent(self, event):
		# Now grab the word under the cursor, first
		# get the cursor for the event position
		cursor = self.cursorForPosition(event.pos())
		cursor.movePosition(QtGui.QTextCursor.StartOfWord)
		cursor.movePosition(QtGui.QTextCursor.EndOfWord, mode=QtGui.QTextCursor.KeepAnchor)
		# Set the extra selection
		self.set_extra_selection_from_cursor(cursor)
		# set the double click flag
		self.has_just_double_clicked = True

	def mouseMoveEvent(self, event):
		self.has_just_selected = True
		# if event.button() == QtCore.Qt.LeftButton:
		cursor = self.cursorForPosition(event.pos())
		# new_cursor_block_position = cursor.block().position()
		new_cursor_position = cursor.position()
		# Select text between the old and new positions and copy to clipboard
		# if the positions are different
		if self.old_cursor_pos.position() != new_cursor_position:
			cursor.setPosition(self.old_cursor_pos.position())
			cursor.setPosition(new_cursor_position, mode=QtGui.QTextCursor.KeepAnchor)
			self.set_extra_selection_from_cursor(cursor)
			# Set the vertical scroll bar to be where the mouse cursor is
			# self.verticalScrollBar().setValue(new_cursor_block_position) #self.verticalScrollBar().maximum())
	
	# Here we sort out all the keypress events, need to 
	# test for keys that we are pressing and act accordingly
	def keyPressEvent(self, event):
		key_pressed = event.key()
		# First ignore any keys in the ignore
		# list
		if key_pressed in self.IGNORE_KEYS:
			pass
		# Handle return on the shell - execute command
		elif key_pressed == QtCore.Qt.Key_Return:
			if self.pii_completer and self.pii_completer.is_visible():
				event.ignore() # Ignoring the enter keypress here makes qt fall back and use the completer event
			else:
				self.handle_enter()
		# Handle cursor move up - go backwards through command history
		elif key_pressed == QtCore.Qt.Key_Up:
			self.handle_up()
		# Handle cursor move up - go forwards through command history
		elif key_pressed == QtCore.Qt.Key_Down:
			self.handle_down()
		# Handle cursor move left - default behaviour unless at start of line
		elif key_pressed == QtCore.Qt.Key_Left and self.at_command_start():
			pass
		# Handle backspace - default behaviour unless at start of line
		elif key_pressed == QtCore.Qt.Key_Backspace and self.at_command_start():
			pass
		# Handle Home press - jumps to start of line (after prompt)
		elif key_pressed == QtCore.Qt.Key_Home:
			self.handle_home()
		elif key_pressed == QtCore.Qt.Key_Escape:
			self.pii_completer.hide_if_visible()
		# All other key presses default to normal behaviour
		else:
			super(PiiTerminal, self).keyPressEvent(event)
			# First get the text under and before the cursor
			# This must happen AFTER the super has been called
			text_under = str(self.get_text_under_cursor())
			text_before = str(self.get_text_before_cursor())
			# Update the completer and show it
			self.update_completer(self.text_enter_direction(key_pressed))
			# enter_forward = bool(key_pressed != QtCore.Qt.Key_Backspace)
			# self.update_completer(text_under, text_before, forward=enter_forward)
			self.show_completer(text_under, text_before)
			# Reset the command history position
			self.command_history.reset_history_position()

	#========================================================================
	# Methods that manipulate the widget completer
	#========================================================================

	def get_completer(self, matching_list):
		return completer.PiiAutoCompleter(matching_list, widget=self, font=self.text_editor_font, on_completion=self.replace_text_under_cursor)

	def update_completer(self, text_direction):
		# Text direction can be either "backwards"
		# or "forwards"
		module_hierarchy = self.get_module_hierarchy_under_cursor()
		# If text_under is "", then we have three possible situations
		# 1) text_before == "." -> update to complete on module
		if self.text_enter_module():
			module_dir = ".".join(module_hierarchy)
			module_list = self.pii_interpreter.get_local_dir(module_dir)
			self.pii_completer.update_matches(module_list)
		# 2) text_before == "(" -> update to show doc string of function
		elif self.text_enter_function():
			self.pii_completer.hide_if_visible()
			module_fn = ".".join(module_hierarchy).strip("(")
			docstring = self.pii_interpreter.get_object_docstring(module_fn)
			QtGui.QToolTip.showText(self.get_text_cursor_position(), docstring)
		# 3) text_before != "(" or "." -> update to complete from locals
		elif self.at_prompt() or self.text_under_empty() or (self.text_under_eq_text_before() and len(module_hierarchy) == 1 ):
			self.pii_completer.update_matches(self.pii_interpreter.get_local_list())

	def show_completer(self, text_under, text_before):
		# Here we always update the completion prefix
		self.pii_completer.setCompletionPrefix(text_under)
		# Only show the completer popup if we have text under the cursor
		if text_under or self.text_enter_module():
			popup = self.pii_completer.popup()
			popup.setCurrentIndex(self.pii_completer.completionModel().index(0,0))
			cr = self.cursorRect()
			cr.setWidth(self.pii_completer.popup().sizeHintForColumn(0) + self.pii_completer.popup().verticalScrollBar().sizeHint().width())
			self.pii_completer.complete(cr) ## popup it up!
		elif self.text_enter_function():
			self.pii_completer.hide_if_visible()

	#========================================================================
	# Other Misc class methods
	#========================================================================

	def print_welcome_msg(self):
		self.insertPlainText("Welcome to PII - Python Interactive Interpreter")
		self.insert_line_break(1)
		self.insertPlainText("Running Python {version_info} on {platform}".format(**self.WELCOME_FORMAT_DICT))
		self.insert_line_break(2)

	@contextmanager
	def use_multiline_prompt(self, prompt=None):
		self.user_prompt = prompt if prompt else self.PS2
		try:
			yield
		finally:
			self.user_prompt = self.PS1

	def write_user_prompt(self, format=None):
		self.insertPlainText(self.user_prompt)
		format = format if format else PiiTextFormats().BOLD
		tc = self.textCursor()
		tc.movePosition(QtGui.QTextCursor.StartOfLine)
		tc.select(QtGui.QTextCursor.WordUnderCursor)
		tc.mergeCharFormat(format)

	def initialise_interpreter(self):
		self.pii_interpreter = interpreter.PiiInterpreter()

	def initialise_tooltip(self):
		QtGui.QToolTip.setFont(self.text_editor_font)

	def setup_text_edit_font(self, size=None):
		font_size = size if size else self.font_point_size
		self.text_editor_font = QtGui.QFont()
		self.text_editor_font.setFamily("Monospace")
		self.text_editor_font.setStyleHint(QtGui.QFont.TypeWriter)
		self.text_editor_font.setFixedPitch(True)
		self.text_editor_font.setPointSize(font_size)

	def at_command_start(self):
		return(self.textCursor().position() == self.textCursor().block().position() + len(self.user_prompt))

	def at_prompt(self):
		text_before = str(self.get_text_before_cursor())
		return (text_before == self.user_prompt.rstrip())

	def on_user_prompt_line(self, cursor):
		cursor.movePosition(QtGui.QTextCursor.StartOfLine)
		cursor.select(QtGui.QTextCursor.WordUnderCursor)
		prompt = str(cursor.selectedText()) + " "
		return (prompt in [self.PS1, self.PS2])

	def get_module_hierarchy_under_cursor(self):
		# Get the line of text from the cursor pos
		# to the beginning of the line
		line_text = self.get_command()
		line_items = line_text.split()
		line_position = self.get_text_cursor_position_in_line()
		line_item_range = []
		_range = 0
		for item in line_items:
			_range += len(item)+1
			line_item_range.append(_range)
		line_position = self.get_text_cursor_position_in_line()
		current_word = ""
		for r in line_item_range:
			if line_position < r:
				current_word = line_items[line_item_range.index(r)]
				break

		return [ w for w in current_word.split(".") if w ]

	def get_text_cursor_position_in_line(self):
		prompt_length = len(self.user_prompt)
		block_start_pos = self.textCursor().block().position()
		cursor_pos = self.textCursor().position()
		return (cursor_pos - block_start_pos - prompt_length)

	def clear_text_from_line(self):
		# Get the start pos and end pos
		start_pos = self.textCursor().block().position() + len(self.user_prompt)
		self.moveCursor(QtGui.QTextCursor.EndOfLine)
		end_pos = self.textCursor().position()
		# Select the line
		if start_pos != end_pos:
			cursor = self.textCursor()
			cursor.setPosition(start_pos);
			cursor.setPosition(end_pos, QtGui.QTextCursor.KeepAnchor);
			self.setTextCursor(cursor)
			# Delete the current selection
			self.textCursor().deleteChar()
			# Move the cursor the start of the line
			self.move_to_line_start(str_prefix=self.user_prompt)

	def replace_current_text(self, text):
		self.clear_text_from_line()
		self.insertPlainText(text)

	def get_command(self):
		line_text = str(self.textCursor().block().text())
		command_text = line_text.replace(self.user_prompt, "")
		if command_text == "\t":
			command_text = ""
		return command_text

	def handle_home(self):
		self.move_to_line_start(str_prefix=self.user_prompt)

	def handle_up(self):
		cmd = self.command_history.get_prev_command()
		self.replace_current_text(cmd)

	def handle_down(self):
		cmd = self.command_history.get_next_command()
		self.replace_current_text(cmd)

	def handle_enter(self):
		# Run the command loop
		self.is_multiline = self.run_command(self.is_multiline)
		if self.is_multiline:
			with self.use_multiline_prompt():
				self.write_user_prompt(format=PiiTextFormats().BOLD_RED)
			self.insert_tab(1)
		else:
			# Insert some spaceage
			self.insert_line_break(2)
			# Add a prompt
			self.write_user_prompt(format=PiiTextFormats().BOLD_RED)
		# Now move to the end of the scroll box
		self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

	def run_command(self, multiline):
		# Get the command from the line
		if multiline:
			with self.use_multiline_prompt():
				command_text = self.get_command()
		else:
			command_text = self.get_command()
		# Pre-empt any multilines so we can display stuff
		# before the result
		is_multiline = False
		if command_text.endswith(":"):
			multiline = True
		self.move_to_line_end()
		self.insert_line_break(1)
		# If not a multiline then print a result prompt
		# The or here ensures that the post result prompt 
		# is displayed after the end of a multiline segment
		if not multiline or (multiline and not command_text):
			with self.use_multiline_prompt(prompt=self.RESULT_PROMPT):
				self.write_user_prompt(format=PiiTextFormats().BOLD_GREEN)
				self.insert_line_break(1)

		# if not multiline:
		with redirect_stdout_and_stderr(self):
			is_multiline = self.execute_command(command_text)

		# Update the command history
		self.command_history.add_to_history(command_text)
		return is_multiline

	def execute_command(self, cmd):
		return self.pii_interpreter.push(cmd)