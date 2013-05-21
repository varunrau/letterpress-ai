from board import Board

class Player:

	def __init__(self, depth=3):
		self.depth = depth

	def makeMove(self, board):
		return self.getMove(board)

	def getMove(self, board):

		def maxAgent(state, depth, alpha, beta):
			if state.isGameOver():
				return state.getScore()
			actions = state.getLegalWords()
			best_score = float("-inf")
			score = best_score
			best_action = actions.pop(0)
			for action in actions:
				newState = copy.deepcopy(state)
				score = minAgent(newState.generateSuccessor(action, "BLUE"), depth, alpha, beta)
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
				return state.getScore()
			actions = state.legalMoves()
			best_score = float("inf")
			score = best_score
			for action in actions:
				if depth == self.depth - 1:
					newState = copy.deepcopy(state)
					score = self.evalBoard(newState.generateSuccessor(action, "RED"))
				else:
					newState = copy.deepcopy(state)
					score = maxAgent(newState.generateSuccessor(action, "RED"), depth + 1, alpha, beta)
				if score < best_score:
					best_score = score
				beta = min(beta, best_score)
				if best_score < alpha:
					return best_score
			return best_score

		return maxAgent(board, 0, float("-inf"), float("inf"))




