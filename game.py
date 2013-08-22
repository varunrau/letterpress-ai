"""
This is a sample program that shows how to use the letterpress AI.
It plays a game of letterpress between two of the AI.
"""

from board import Board
from player import MachinePlayer, HumanPlayer
import json

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

def returnMove(gameJson):
	game = json.loads(gameJson)
	board = Board(game)
	player = MachinePlayer()
	move = player.getMove(board)
	print move
	return move


if __name__ == "__main__":
	board = Board()
	player1 = MachinePlayer("BLUE", "RED")
	player2 = MachinePlayer("RED", "BLUE")
	play(board, player1, player2)

