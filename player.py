import globals
from board import Board
from util import SimpleVector, PriorityQueueWithFunction
import copy

class Player:
	"""
	The AI that plays letterpress. Powered by the minimax algorithm with alpha-beta pruning.
	"""

	def __init__(self, team, opponent, depth=globals.DEPTH):
		"""
		Constructs an AI.
		@param team - the team of the player.
		@param opponent - the team of the opponent.
		@param depth - the depth to run minimax. Defaults to whatever is in globals.py.
		"""
		self.depth = depth
		self.team = team
		self.opponent = opponent


	def getMove(self, board):
		"""
		The main interface with AI. Returns a move to play.
		Runs minimax with alpha-beta pruning.
		@param board - the current board.
		@return the AI's move.
		"""
		def maxAgent(state, depth, alpha, beta):
			if state.isGameOver():
				return self.evalBoard(state)
			actions = state.getLegalMovesWithPriority(self.evalMove, globals.SIZE, self.team)
			best_score = float("-inf")
			score = best_score
			best_action = actions.get()
			while not actions.isEmpty():
				action = actions.pop()
				newState = copy.deepcopy(state).generateSuccessor(action, self.team)
				score = minAgent(newState, depth, alpha, beta)
				del newState
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
			actions = state.getLegalMovesWithPriority(self.evalMove, globals.SIZE, self.opponent)
			best_score = float("inf")
			score = best_score
			best_action = actions.get()
			while not actions.isEmpty():
				action = actions.pop()
				if depth == self.depth - 1:
					newState = copy.deepcopy(state).generateSuccessor(action, self.opponent)
					score = self.evalBoard(newState)
					del newState
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
		"""
		The evaluation of the board. This method is used when depth is reached in minimax.
		@param board - the board to evaluate.
		@return an floating point evaluation.
		"""

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
		"""
		A weight vector for the board evaluation.
		@return A SimpleVector object used for board evaluation.
		"""
		weights = SimpleVector()
		weights["protected"] = 1
		weights["oppProtected"] = -1
		weights["tilesLeft"] = 1
		weights["score"] = 1
		weights.normalize()
		return weights

	def evalMove(self, args):
		"""
		Evalutation of a move. This method is used as a priority function for ordering
		potential moves.
		@param args - the arguments of the function
		(the current board, the move to evaluate, the team).
		@return a floating point evaluation
		"""
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
		"""
		The weight vector used to evaluate a move.
		@return a SimpleVector object of move weights.
		"""
		weights = SimpleVector()
		weights["length"] = 1
		weights["scoreDifference"] = 1
		weights["protectedDifference"] = 2
		weights["oppProtectedDiffernece"] = -1
		weights["tilesLeftDifference"] = 0
		weights.normalize()
		return weights


