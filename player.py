from board import Board
from util import SimpleVector, PriorityQueueWithFunction
import copy

class Player:

	def __init__(self, team, opponent, depth=1):
		self.depth = depth
		self.team = team
		self.opponent = opponent

	def makeMove(self, board):
		return self.getMove(board)

	def getMove(self, board):
		def maxAgent(state, depth, alpha, beta):
			if state.isGameOver():
				return self.evalBoard(state)
			actions = state.getLegalMovesWithPriority(self.evalMove, 50, self.team)
			best_score = float("-inf")
			score = best_score
			best_action = actions.get()
			while not actions.isEmpty():
				action = actions.pop()
				newState = copy.deepcopy(state).generateSuccessor(action, self.team)
				score = minAgent(newState, depth, alpha, beta)
				if score > best_score:
					best_score = score
					best_action = action
				alpha = max(alpha, best_score)
				if best_score > beta:
					return best_score
			if depth == 0:
				return best_action
			else:
				return best_score

		def minAgent(state, depth, alpha, beta):
			if state.isGameOver():
				return self.evalBoard(state)
			actions = state.getLegalMovesWithPriority(self.evalMove, 50, self.opponent)
			best_score = float("inf")
			score = best_score
			best_action = actions.get()
			while not actions.isEmpty():
				action = actions.pop()
				if depth == self.depth - 1:
					newState = copy.deepcopy(state).generateSuccessor(action, self.opponent)
					score = self.evalBoard(newState)
				else:
					newState = copy.deepcopy(state)
					score = maxAgent(newState.generateSuccessor(action, self.opponent), depth + 1, alpha, beta)
				if score < best_score:
					best_score = score
				beta = min(beta, best_score)
				if best_score < alpha:
					return best_score
			return best_score

		return maxAgent(board, 0, float("-inf"), float("inf"))

	def evalBoard(self, board):

		def protected():
			return sum([1 for letter in board.getLetters() if letter.color == self.team and letter.protected])

		def oppProtected():
			return sum([1 for letter in board.getLetters() if letter.color != self.team and letter.protected])

		def tilesLeft():
			return sum([1 for letter in board.getLetters() if not letter.color.isAssigned()])

		def score():
			return board.getScore(self.team)

		weights = self.getBoardWeightVector()
		features = SimpleVector()

		for feature in weights:
			features[feature] = eval(feature)()

		return features * weights

	def getBoardWeightVector(self):
		weights = SimpleVector()
		weights["protected"] = 1
		weights["oppProtected"] = -1
		weights["tilesLeft"] = 1
		weights["score"] = 1
		weights.normalize()
		return weights

	def evalMove(self, args):
		board, move, team = args

		def length():
			return len(move.getWord())
		def scoreDifference():
			originalScore = board.getScore(team)
			newBoard = copy.deepcopy(board)
			newBoard.makeMove(move, team)
			newScore = newBoard.getScore(team)
			return newScore - originalScore
		def protectedDifference():
			original = sum([1 for letter in board.getLetters() if letter.protected and letter.color == team])
			newBoard = copy.deepcopy(board)
			newBoard.makeMove(move, team)
			new = sum([1 for letter in newBoard.getLetters() if letter.protected and letter.color == team])
			return new - original
		def oppProtectedDiffernece():
			original = sum([1 for letter in board.getLetters() if letter.protected and not letter.color == team])
			newBoard = copy.deepcopy(board)
			newBoard.makeMove(move, team)
			new = sum([1 for letter in newBoard.getLetters() if letter.protected and not letter.color == team])
			return new - original
		def tilesLeftDifference():
			original = sum([1 for letter in board.getLetters() if not letter.color.isAssigned()])
			newBoard = copy.deepcopy(board)
			newBoard.makeMove(move, team)
			new = sum([1 for letter in newBoard.getLetters() if not letter.color.isAssigned()])
			return new - original

		weights = self.getMoveWeightVector()
		features = SimpleVector()
		for feature in weights:
			features[feature] = eval(feature)()
		return features * weights

	def getMoveWeightVector(self):
		weights = SimpleVector()
		weights["length"] = 1
		weights["scoreDifference"] = 1
		weights["protectedDifference"] = 1
		weights["oppProtectedDiffernece"] = 1
		weights["tilesLeftDifference"] = 1
		weights.normalize()
		return weights

