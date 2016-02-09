#========================================================================
# Command Line History
#========================================================================
class PiiCommandHistory(object):
	def __init__(self, max_length=1000):
		self.max_length = max_length
		self.command_list = []
		self.history_pos = -1

	def add_to_history(self, command):
		if len(self.command_list) > self.max_length:
			self.command_list.pop(0)
		if command:
			self.command_list.append(command)
		self.reset_history_position()

	def get_prev_command(self):
		if self.history_pos > 0:
			self.history_pos -= 1
		return self.command_list[self.history_pos]

	def get_next_command(self):
		if self.history_pos >= len(self.command_list)-1:
			return ""
		else:
			self.history_pos += 1
			return self.command_list[self.history_pos]

	def reset_history_position(self):
		self.history_pos = len(self.command_list)

	def clear_history(self):
		self.command_list = []
		self.history_pos = -1