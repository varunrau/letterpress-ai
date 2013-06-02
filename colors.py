
class Color:
	"""
	A class useful for drawing on the terminal with color.
	Tested on Mac OS X (iTerm 2).
	"""

	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	RED = '\033[91m'
	END = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

