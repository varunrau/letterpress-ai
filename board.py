import random
from letter import Letter
from side import Side

class Board():

	def __init__(self, letters=[]):
		self.SIZE = 5
		self.letters = letters
		self.played_words = set()
		if isinstance(self.letters, basestring):
			self.parseString()
		else:
			self.randomizeLetters()

	def generateSuccessor(self, word, team):
		if self.isLegalMove(word):
			self.makeMove(word, team)
			return self
		return "CANT GENERATE SUCCESSOR"


	def parseString(self):
		string = self.letters
		self.letters = []
		for x in range(5):
			self.letters.append([])
			for y in range(5):
				self.letters.append(string.pop(0))



	def randomizeLetters(self):
		for x in range(self.SIZE):
			self.letters.append([])
			for y in range(self.SIZE):
				self.letters[x].append(Letter())

	def getLetters(self):
		lettersList = []
		for row in self.letters:
			for letter in row:
				lettersList.append(letter)
		return lettersList


	def isLegalMove(self, word):
		lettersList = self.getLetters()
		for letter in word:
			if letter in lettersList:
				lettersList.remove(letter)
			else:
				return False
		for played_word in self.played_words:
			if word == played_word:
				return False
			if len(word) < len(played_word):
				for x in range(len(word)):
					if word[x:] == played_word
						return False
		# Include check in letterpress' big list of words
		return True


	def makeMove(self, word, side):
		if self.isLegalMove(word):
			for letter in word:
				self.letters[letter.position[0]][letter.position[1]].changeTeam(side)
			self._updateProtected()
		else:
			print "ILLEGAL MOVE"




	def isGameOver(self):
		#usedLetters = 0
		#for letter in self.letters:
			#if letter.color is not None:
				#usedLetters += 1
		return sum(1 for i in self.letters if i.color is not None) == self.SIZE * self.SIZE


	def isWin(self):
		teams = {}
		for letter in self.letters:
			if letter.color is not None:
				if teams[letter.color]:
					teams[letter.color] += 1
				else:
					teams[letter.color] = 1
		for team in teams:
			if teams[team] > self.SIZE * self.SIZE / 2:
				return team
		return None



	def legalMoves():
		legalWords = []
		words = open("word-list/Words/en.txt", "r")
		for word in words:
			if self.isLegalMove(word):
				legalWords.append(word)
		return legalWords



	def _updateProtected(self):
		for rowIndex, row in enumerate(self.letters):
			for colIndex, letter in enumerate(row):
				letterNeighbors = self.getNeighbors(letter, (rowIndex, colIndex))
				count = 0
				for neighbor in letterNeighbors:
					if neighbor.color == letter.color and letter.color is not None:
						count += 1
				letter.protected = len(letterNeighbors) == count


	def getNeighbors(self, letter, letterPos):
		neighbors = []
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if abs(dx) + abs(dy) > 1 or dx + dy == 0:
					continue
				neighborPos = (letterPos[0] + dx, letterPos[1] + dy)
				if neighborPos[0] >= 0 and neighborPos[0] < self.SIZE \
						and neighborPos[1] >= 0 and neighborPos[1] < self.SIZE:
					neighbors.append(self.letters[neighborPos[0]][neighborPos[1]])
		return neighbors


	def __repr__(self):
		string = ""
		for row in self.letters:
			string += "["
			for letter in row:
				string += " "
				string += str(letter)
				string += " "
			string += "]\n"
		return string


board = Board()
print board


l1 = Letter((0,0))
l2 = Letter((1,0))
l3 = Letter((0,1))

l1.value = board.letters[0][0].value
l2.value = board.letters[1][0].value
l3.value = board.letters[0][1].value
move = [l1, l2, l3]

l4 = Letter((0,0))
l5 = Letter((1,0))
l6 = Letter((2,0))

l4.value = board.letters[0][0].value
l5.value = board.letters[1][0].value
l6.value = board.letters[2][0].value
move2 = [l4, l5, l6]

board.makeMove(move, "RED")


import ipdb; ipdb.set_trace() # BREAKPOINT

board.makeMove(move2, "BLUE")
import ipdb; ipdb.set_trace() # BREAKPOINT
