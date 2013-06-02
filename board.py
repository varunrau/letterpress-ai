import random
from letter import Letter
from side import Side
from move import Move
from util import PriorityQueueWithFunction
import globals
import copy

class Board():
	"""
	A representation of a letterpress board.
	"""

	def __init__(self, letters=[]):
		"""
		Initialize the board.
		@param letters - Initialize the board with letters. These can be a
		matrix of letter of objects or a string. Optional.
		"""
		self.SIZE = globals.SIZE
		self.letters = letters
		self.played_words = set()
		self.rules = ["self.availableLetter", "self.repeatPlay"]
		if isinstance(self.letters, basestring):
			self.parseString()
		else:
			self.randomizeLetters()
		self.possibleWords = set()
		self.calcPossibleWords()


	def generateSuccessor(self, word, team):
		"""
		Generates the successor to this board after playing word.
		@param word - the word to play. A move object.
		@param team - the team that is playing that word. String.
		@return a board object.
		"""
		self.makeMove(word, team)
		self._updateLegalMoves()
		return self


	def getScore(self, team):
		"""
		The current score based on the team. Based on the way the Letterpress app scores.
		@param team - the team's score. String.
		@return the Letterpress score of the board for the team.
		"""
		teamScore = sum([1 for i in self.getLetters() if i.color == team])
		otherScore = sum([1 for i in self.getLetters() if not i.color == team and not i.color.isAssigned()])
		return teamScore - otherScore

	def parseString(self):
		"""
		Reevaluates the board's letters from a string representation to a matrix representation.
		"""
		string = []
		for letter in self.letters:
			string.append(letter)
		self.letters = []
		for x in range(self.SIZE):
			self.letters.append([])
			for y in range(self.SIZE):
				self.letters[x].append(Letter((x,y), string.pop(0)))


	def randomizeLetters(self):
		"""
		Calculates new random letters for the board.
		"""
		for x in range(self.SIZE):
			self.letters.append([])
			for y in range(self.SIZE):
				self.letters[x].append(Letter((x,y)))

	def getLetters(self):
		"""
		The board's letters. Returned as a list.
		@return a list of the board's letters
		"""
		lettersList = []
		for row in self.letters:
			for letter in row:
				lettersList.append(letter)
		return lettersList


	def isLegalMove(self, move):
		"""
		True iff the move is legal.
		@param move - the move to consider.
		@return boolean for whether the move is legal.
		"""
		for rule in self.rules:
			if not eval(rule)(move):
				return False
		return True


	def availableLetter(self, move):
		"""
		One of Letterpress's rules. True iff the board has all the letters that the move
		needs.
		@param move - the move to consider.
		@return true iff this rule is statisfied.
		"""
		lettersList = self.getLetters()
		word = move.getWord()
		for letter in word:
			if letter in lettersList:
				lettersList.remove(letter)
			else:
				return False
		return True

	def repeatPlay(self, move):
		"""
		One of Letterpress' rules. True iff the word has not been played before and
		this word is not a prefix of a previously played word.
		@param move - the move to consider. A move object.
		@return true iff this rule is satisfied.
		"""
		word = move.getWord()
		for played_move in self.played_words:
			played_word = played_move.getWord()
			if move == played_move:
				return False
			if len(word) < len(played_word):
				for x in range(len(played_word)):
					if played_word[:x] == word:
						return False
		return True

	def makeMove(self, word, side):
		"""
		Plays the move provided.
		@param word - the word to play. This must be a move object.
		@param side - the side to play for. String.
		"""
		if self.isLegalMove(word):
			for letter in word.getWord():
				self.letters[letter.position[0]][letter.position[1]].changeTeam(side)
			self._updateProtected()
			self.played_words.add(word)


	def isGameOver(self):
		"""
		Checks if the game is over.
		@return True iff all the letters are assigned a color.
		"""
		return sum([1 for i in self.getLetters() if i.color.isAssigned()]) == self.SIZE * self.SIZE


	def isWin(self):
		"""
		Checks to see if the game is over and returns the winner.
		@return the winning team. String.
		"""
		teams = {}
		for letter in self.getLetters():
			if letter.color.isAssigned():
				colorString = str(letter.color)
				if colorString in teams:
					teams[colorString] += 1
				else:
					teams[colorString] = 1
		for team in teams:
			if teams[team] > self.SIZE * self.SIZE / 2:
				return team
		return None


	def getLegalMoves(self):
		"""
		All the legal words to play for this board.
		Note: This method is rarely useful because the list will in most cases be too large to process
		in a reasonable amount of time.
		@return a list of all legal moves.
		"""
		legalWords = []
		for word in self.possibleWords:
			if self.isLegalMove(word):
				legalWords.append(word)
		return legalWords

	def getLegalMovesWithPriority(self, priorityFunction, n, team):
		"""
		The first n legal moves to play for this board ordered by the
		priority given to it by the priority function.
		@param priorityFunction - a function that assigns a priority to a move.
		It must accept a board, move, and string as parameters.
		@param n - the number of moves to return
		@param team - the team. Note: this parameter is not needed to return legality of moves
		but it is useful for ordering them.
		@return a list of n legal moves
		"""
		legalWords = PriorityQueueWithFunction(priorityFunction)
		for word in self.possibleWords:
			if len(legalWords) >= n:
				return legalWords
			if self.isLegalMove(word):
				legalWords.push(self, word, team)
		return legalWords


	def calcPossibleWords(self):
		"""
		Initialization method. Used to calculate all the possible moves
		on the board based on the current board.
		"""
		legalWords = set()
		words = open("word-list/Words/en.txt", "r")
		for word in words:
			cleanWord = "".join(letter for letter in word if letter.isalnum())
			legalMovesFromWord = self.getLegalMovesFromWord(cleanWord)
			if len(legalMovesFromWord) > 0:
				for move in legalMovesFromWord:
					if self.isLegalMove(move):
						legalWords.add(move)
		self.possibleWords = legalWords


	def getLegalMovesFromWord(self, word):
		"""
		Returns all legal moves for a given word.
		@param word - the word to get legal moves from. A String.
		@return a list of all legal moves (move objects) for this board.
		"""
		tilesForLetter = {}

		def calcTilesForLetter():
			for tile in self.getLetters():
				for letter in set(word):
					if tile.value == letter:
						if letter not in tilesForLetter:
							tilesForLetter[letter] = [tile]
						else:
							tilesForLetter[letter].append(tile)

		def findLegal(play):
			if len(play) == 0:
				return []
			if len(play) == 1:
				newPlay = []
				for tile in tilesForLetter[play[0]]:
					newPlay.append([tile])
				return newPlay
			plays = []
			for tile in tilesForLetter[play[0]]:
				for ending in findLegal(play[1:]):
					ending.insert(0, tile)
					plays.append(ending)
			return plays

		def possibleWord(play):
			for letter in word:
				letterCount = sum([1 for otherletter in word if letter == otherletter])
				tileCount = sum([1 for tile in self.getLetters() if tile.value == letter])
				if letterCount > tileCount:
					return False
			return True

		if possibleWord(word):
			calcTilesForLetter()
			return [Move(w) for w in findLegal(word)]
		else:
			return []


	def _updateProtected(self):
		for rowIndex, row in enumerate(self.letters):
			for colIndex, letter in enumerate(row):
				letterNeighbors = self._getNeighbors(letter, (rowIndex, colIndex))
				count = 0
				for neighbor in letterNeighbors:
					if neighbor.color == letter.color and letter.color is not None:
						count += 1
				letter.protected = len(letterNeighbors) == count

	def _updateLegalMoves(self):
		legalWords = set()
		for word in self.possibleWords:
			if self.isLegalMove(word):
				legalWords.add(word)
		self.possibleWords = legalWords
		return legalWords


	def _getNeighbors(self, letter, letterPos):
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
		"""
		The representation of the board.
		@return a string that represents the board.
		"""
		string = ""
		for row in self.letters:
			string += "["
			for letter in row:
				string += " "
				string += str(letter)
				string += " "
			string += "]\n"
		return string

