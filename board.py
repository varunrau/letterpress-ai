import random
from letter import Letter
from side import Side
from move import Move
from util import PriorityQueueWithFunction
import copy

class Board():

	def __init__(self, letters=[]):
		self.SIZE = 5
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
		self.makeMove(word, team)
		self._updateLegalMoves()
		return self


	def getScore(self, team):
		teamScore = sum([1 for i in self.getLetters() if i.color == team])
		otherScore = sum([1 for i in self.getLetters() if not i.color == team and not i.color.isAssigned()])
		return teamScore - otherScore

	def parseString(self):
		string = []
		for letter in self.letters:
			string.append(letter)
		self.letters = []
		for x in range(self.SIZE):
			self.letters.append([])
			for y in range(self.SIZE):
				self.letters[x].append(Letter((x,y), string.pop(0)))


	def randomizeLetters(self):
		for x in range(self.SIZE):
			self.letters.append([])
			for y in range(self.SIZE):
				self.letters[x].append(Letter((x,y)))

	def getLetters(self):
		lettersList = []
		for row in self.letters:
			for letter in row:
				lettersList.append(letter)
		return lettersList


	def isLegalMove(self, move):
		for rule in self.rules:
			if not eval(rule)(move):
				return False
		return True


	def availableLetter(self, move):
		lettersList = self.getLetters()
		word = move.getWord()
		for letter in word:
			if letter in lettersList:
				lettersList.remove(letter)
			else:
				return False
		return True

	def repeatPlay(self, move):
		#string = ""
		#for letter in move.getWord():
			#string += str(letter.value)
		#print string
		#if string == "ja":
			#import ipdb; ipdb.set_trace() # BREAKPOINT
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
		if self.isLegalMove(word):
			for letter in word.getWord():
				self.letters[letter.position[0]][letter.position[1]].changeTeam(side)
			self._updateProtected()
			self.played_words.add(word)
		#else:
			#print "ILLEGAL MOVE"


	def isGameOver(self):
		return sum([1 for i in self.getLetters() if i.color.isAssigned()]) == self.SIZE * self.SIZE


	def isWin(self):
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
		legalWords = []
		for word in self.possibleWords:
			if self.isLegalMove(word):
				legalWords.append(word)
		return legalWords

	def getLegalMovesWithPriority(self, priorityFunction, n, team):
		legalWords = PriorityQueueWithFunction(priorityFunction)
		for word in self.possibleWords:
			if len(legalWords) >= n:
				return legalWords
			if self.isLegalMove(word):
				legalWords.push(self, word, team)
		return legalWords


	def calcPossibleWords(self):
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
				letterNeighbors = self.getNeighbors(letter, (rowIndex, colIndex))
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

