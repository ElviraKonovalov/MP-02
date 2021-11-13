# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np
from skimage.util import view_as_windows

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, recommend = True):
		# self.initialize_game()
		self.recommend = recommend
		
	def initialize_game(self):
		# n = 3
		# self.current_state = np.array([['.','.','.'],
		# 					  ['.','.','.'],
		# 					  ['.','.','.']])
		self.current_state = np.full([n, n], '.', dtype='str_')
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		# n = 3
		print()
		for y in range(0, n):
			for x in range(0, n):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > 2 or py < 0 or py > 2:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def isin_seq_v2(self, a, b):
		return (view_as_windows(a,len(b))==b).all(1).any()

	def e1(self, x, y):
		s = 3
		V = 0

		max_col = len(self.current_state[0])
		max_row = len(self.current_state)
		cols = [[] for _ in range(max_col)]
		rows = [[] for _ in range(max_row)]
		fdiag = [[] for _ in range(max_row + max_col - 1)]
		bdiag = [[] for _ in range(len(fdiag))]
		min_bdiag = -max_row + 1

		for x in range(max_col):
		    for y in range(max_row):
		        cols[x].append(self.current_state[y][x])
		        rows[y].append(self.current_state[y][x])
		        fdiag[x+y].append(self.current_state[y][x])
		        bdiag[x-y-min_bdiag].append(self.current_state[y][x])
		        
		for row in rows:
		    for num in range(s,0,-1):
		        if num == np.count_nonzero(np.array(row) == 'X'):
		            V += (num*100)
		            break
		        else:
		            if num == np.count_nonzero(np.array(row) == 'O'):
		                V -= (num*100)
		                break

		for col in cols:
		    for num in range(s,0,-1):
		        if num == np.count_nonzero(np.array(col) == 'X'):
		            V += (num*100)
		            break
		        else:
		            if num == np.count_nonzero(np.array(col) == 'O'):
		                V -= (num*100)
		                break

		for f in fdiag:
		    for num in range(s,0,-1):
		        if num == np.count_nonzero(np.array(f) == 'X'):
		            V += (num*100)
		            break
		        else:
		            if num == np.count_nonzero(np.array(f) == 'O'):
		                V -= (num*100)
		                break

		for b in bdiag:
		    for num in range(s,0,-1):
		        if num == np.count_nonzero(np.array(b) == 'X'):
		            V += (num*100)
		            break
		        else:
		            if num == np.count_nonzero(np.array(b) == 'O'):
		                V -= (num*100)
		                break
		# print(V)
		return V

	def is_end(self):
		# n = 3
		s = 3
		# Vertical win
		print("checking if game is ending...")    
		for j in range(0, n):
		    cons_pieces = 0
		    for i in range(0, n):
		        if self.current_state[i][j] != "-" and (i+1) < n and self.current_state[i][j] != '.':
		            # print("current_state[i][j]='",self.current_state[i][j],"' current_state[i+1][j]='",self.current_state[i+1][j],"'")
		            if self.current_state[i][j] == self.current_state[i+1][j]:
		                cons_pieces += 1
		            if cons_pieces != 0 and self.current_state[i][j] != self.current_state[i+1][j]:
		                cons_pieces = 0
		        if cons_pieces+1 >= s:
		            return self.current_state[i][j]

		# Horizontal win
		for i in range(0, n):
		    cons_pieces = 0
		    for j in range(0, n):
		        if self.current_state[i][j] != "-" and (j+1) < n and self.current_state[i][j] != '.':
		            if self.current_state[i][j] == self.current_state[i][j+1]:
		                cons_pieces += 1
		            if cons_pieces != 0 and self.current_state[i][j] != self.current_state[i][j+1]:
		                cons_pieces = 0
		        if cons_pieces+1 >= s:
		            return self.current_state[i][j]

		# Diagonal win
		max_col = len(self.current_state[0])
		max_row = len(self.current_state)
		cols = [[] for _ in range(max_col)]
		rows = [[] for _ in range(max_row)]
		fdiag = [[] for _ in range(max_row + max_col - 1)]
		bdiag = [[] for _ in range(len(fdiag))]
		min_bdiag = -max_row + 1

		for x in range(max_col):
		    for y in range(max_row):
		        cols[x].append(self.current_state[y][x])
		        rows[y].append(self.current_state[y][x])
		        fdiag[x+y].append(self.current_state[y][x])
		        bdiag[x-y-min_bdiag].append(self.current_state[y][x])

		s_cons_x = np.full(s, "X", dtype='str_')
		s_cons_o = np.full(s, "O", dtype='str_')   
	        
		for f in fdiag:
		    if len(f) >= s:
		        if self.isin_seq_v2(np.array(f), s_cons_x):
		            print('X wins')
		            return 'X'
		        if self.isin_seq_v2(np.array(f), s_cons_o):
		            print('O wins')
		            return 'O'
		for b in bdiag:
		    if len(b) >= s:
		        if self.isin_seq_v2(np.array(b), s_cons_x):
		            print('X wins')
		            return 'X'
		        if self.isin_seq_v2(np.array(b), s_cons_o):
		            print('O wins')
		            return 'O'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def accept_parameters(self):
		n = int(input('the size of the board:'))
		# b = int(input('the number of blocs:'))
		# for i in b:
		# 	bpx = int(input('enter x coordinate for bloc {}):'.format(i)))
		# 	bpy = int(input('enter y coordinate for bloc {}):'.format(i)))
		# 	self.current_state[bpx][bpy]
		# s = int(input('the winning line-up size:'))
		# d1 = int(input('the maximum depth of the adversarial search for player 1:'))
		# d2 = int(input('the maximum depth of the adversarial search for player 2:'))
		# t = int(input('the maximum allowed time (in seconds) for your program to return a move:'))
		# a = input("minimax (FALSE) or alphabeta (TRUE)?")
		# if a == "TRUE":
		# 	a = True
		# if a == "FALSE":
		# 	a = False
		# mode = input('which play mode')
		return n


	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn


	def run_heuristic(self, x, y):
		X_count = np.count_nonzero(self.current_state == 'X')
		O_count = np.count_nonzero(self.current_state == 'O')
		if max:
			return (X_count - O_count)
		else:
			return (O_count - X_count)

	def minimax(self,d, max=False):
		# n = 3
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 10000
		if max:
			value = -10000
		x = None
		y = None
		depth = d

		if depth == 0:
			return (self.e1(x, y), x, y)

		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						# if depth >= 3:
						# 	break
						(v, _, _) = self.minimax(depth-1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						# if depth >= 3:
						# 	break
						(v, _, _) = self.minimax(depth-1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		global n
		n = self.accept_parameters()
		self.initialize_game()
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(2, max=False)
				else:
					(_, x, y) = self.minimax(2, max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)

if __name__ == "__main__":
	main()

