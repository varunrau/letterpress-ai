
class Move:

	def __init__(self, letters):
		self.letters = letters

	def __hash__(self):
		return hash(str(self.letters))

	def getWord(self):
		return self.letters

	def __str__(self):
		return str(self.letters)

	def __eq__(self, otherMove):
		otherWord = otherMove.getWord()
		if not len(self.letters) == len(otherWord):
			return False
		for i in xrange(len(self.letters)):
			if not self.letters[i] == otherWord[i]:
				return False
		return True
