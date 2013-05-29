from board import Board
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
				return 10 * state.getScore(self.team) if self.team == state.isWin() else -1 * state.getScore(self.team)
			actions = state.getLegalMoves()
			best_score = float("-inf")
			score = best_score
			best_action = actions[0]
			for action in actions:
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
				return 10 * state.getScore(self.team) if self.team == state.isWin() else -1 * state.getScore(self.team)
			actions = state.getLegalMoves()
			best_score = float("inf")
			score = best_score
			best_action = actions[0]
			for action in actions:
				if depth == self.depth - 1:
					newState = copy.copy(state)
					score = self.evalBoard(newState.generateSuccessor(action, self.opponent), self.opponent)
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

		def getProtected():
			return sum([1 for letter in board.getLetters() if letter.color == self.team and letter.protected])

		def getOppProtected():
			return sum([1 for letter in board.getLetters() if letter.color != self.team and letter.protected])

		def tilesLeft():
			return sum([1 for letter in board.getLetters() if not letter.color.isAssigned()])

		def score():
			return board.getScore()


		weights = {
				"myProtected" : 1,
				"oppProtected" : 1,
				"tilesLeft" : 1,
				"score" : 1
				}

		features = {
				"myProtected" : 1,
				"oppProtected" : 1,
				"tilesLeft" : 1,
				"score" : 1
				}
		return board.getScore(team)

	#def evalMove(self, board, move, team):




