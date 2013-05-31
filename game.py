from board import Board
from player import Player

def play(board, player1, player2):
	print "LET THE GAME BEGIN\n"
	print board
	isFirstTurn = True
	while not board.isGameOver():
		if isFirstTurn:
			move = player1.getMove(board)
			board.makeMove(move, "BLUE")
			print "Player 1 played " + str(move)
		else:
			move = player2.getMove(board)
			board.makeMove(move, "RED")
			print "Player 2 played " + str(move)
		print board
		isFirstTurn = not isFirstTurn
	print "The winner is " + str(board.isWin())


if __name__ == "__main__":
	board = Board()
	player1 = Player("BLUE", "RED")
	player2 = Player("RED", "BLUE")
	play(board, player1, player2)

