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
		
	def initialize_game(self, n=3):
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
		if px < 0 or px > n-1 or py < 0 or py > n-1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def isin_seq_v2(self, a, b):
		return (view_as_windows(a,len(b))==b).all(1).any()

	def e1(self):
		# s = 3
		# print("---------------board evaluating: \n")
		# self.draw_board()
		V = 0
		# print("V before: ",V)


		max_col = len(self.current_state[0])
		max_row = len(self.current_state)
		cols = [[] for _ in range(max_col)]
		rows = [[] for _ in range(max_row)]
		fdiag = [[] for _ in range(max_row + max_col - 1)]
		bdiag = [[] for _ in range(len(fdiag))]
		min_bdiag = -max_row + 1

		for x in range(max_col):
		    for y in range(max_row):
		        rows[x].append(self.current_state[y][x])
		        cols[y].append(self.current_state[y][x])
		        fdiag[x+y].append(self.current_state[y][x])
		        bdiag[x-y-min_bdiag].append(self.current_state[y][x])
		        
		for row in rows:
			# print(np.array(row))
			for num in range(s,0,-1):
				if num == np.count_nonzero(np.array(row) == 'O'):
					V += (num*100)
					break
				else:
					if num == np.count_nonzero(np.array(row) == 'X'):
						V -= (num*100)
						break
			# print("----V after row evaluation: ",V)

		for col in cols:
			# print(np.array(col))
			for num in range(s,0,-1):
				if num == np.count_nonzero(np.array(col) == 'O'):
				    V += (num*100)
				    break
				else:
					if num == np.count_nonzero(np.array(col) == 'X'):
						V -= (num*100)
						break
			# print("----V after col evaluation: ",V)

		for f in fdiag:
			if len(f) >= s:
				# print(np.array(f))
				for num in range(s,0,-1):
					if num == np.count_nonzero(np.array(f) == 'O'):
						V += (num*100)
						break
					else:
						if num == np.count_nonzero(np.array(f) == 'X'):
							V -= (num*100)
							break
			# print("----V after fdig evaluation: ",V)

		for b in bdiag:
			if len(b) >= s:
				# print(np.array(b))
				for num in range(s,0,-1):
					if num == np.count_nonzero(np.array(b) == 'O'):
						V += (num*100)
						break
					else:
						if num == np.count_nonzero(np.array(b) == 'X'):
							V -= (num*100)
							break
		# 	print("----V after bdig evaluation: ",V)
		# print("V after: ",V)
		# print("-----------")
		return V



	def e2(self):
		V = 0
		# evaluate horizontal potential win for X and O
		for row in range(n):
		    cons_pieces = 0
		    for col in range(n):
		        if self.current_state[row][col] == 'X' or self.current_state[row][col] == '.':
		            cons_pieces += 1
		        else:
		            cons_pieces = 0
		            
		        if cons_pieces >= s:
		            V -= 100
		        
		    cons_pieces = 0
		    for col in range(n):
		        if self.current_state[row][col] == 'O' or self.current_state[row][col] == '.':
		            cons_pieces += 1
		        else:
		            cons_pieces = 0
		            
		        if cons_pieces >= s:
		            V += 100
	    
	    # evaluate vertical potential win for X and O    
		for col in range(n):
		    cons_pieces = 0
		    for row in range(n):
		        if self.current_state[row][col] == 'X' or self.current_state[row][col] == '.':
		            cons_pieces += 1
		        else:
		            cons_pieces = 0
		            
		        if cons_pieces >= s:
		            V -= 100
		        
		    cons_pieces = 0
		    for row in range(n):
		        if self.current_state[row][col] == 'O' or self.current_state[row][col] == '.':
		            cons_pieces += 1
		        else:
		            cons_pieces = 0
		            
		        if cons_pieces >= s:
		            V += 100

		for row in range(n):
		    cons_pieces = 0
		    for col in range(n):
		        r = row
		        c = col
		        while (r+1) < n and (c-1) >= 0:
		            if self.current_state[r][c] == 'X' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r += 1
		            c -= 1

		        r = row
		        c = col     
		        while (r-1) >= 0 and (c+1) < n:
		            if self.current_state[r][c] == 'X' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r -= 1
		            c += 1
		            
		        if cons_pieces >= s:
		            V -= 100
		            
		        r = row
		        c = col
		        while (r-1) >= 0 and (c-1) >= 0:
		            if self.current_state[r][c] == 'X' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r -= 1
		            c -= 1

		        r = row
		        c = col     
		        while (r+1) < n and (c+1) < n:
		            if self.current_state[r][c] == 'X' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r += 1
		            c += 1
		            
		        if cons_pieces >= s:
		            V -= 100
		            
		for row in range(n):
		    cons_pieces = 0
		    for col in range(n):
		        r = row
		        c = col
		        while (r+1) < n and (c-1) >= 0:
		            if self.current_state[r][c] == 'O' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r += 1
		            c -= 1

		        r = row
		        c = col     
		        while (r-1) >= 0 and (c+1) < n:
		            if self.current_state[r][c] == 'O' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r -= 1
		            c += 1
		            
		        if cons_pieces >= s:
		            V += 100
		            
		        r = row
		        c = col
		        while (r-1) >= 0 and (c-1) >= 0:
		            if self.current_state[r][c] == 'O' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r -= 1
		            c -= 1

		        r = row
		        c = col     
		        while (r+1) < n and (c+1) < n:
		            if self.current_state[r][c] == 'O' or self.current_state[r][c] == '.':
		                cons_pieces += 1
		            else:
		                cons_pieces = 0
		            r += 1
		            c += 1
		            
		        if cons_pieces >= s:
		            V += 100
		        
		return V

	def is_end(self):

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

		for i in range(0, n):
			for j in range(0, n):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

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

	def minimax(self, d, start, t, max=False):
		# n = 3
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 1000
		if max:
			value = -1000
		x = None
		y = None
		depth = d

		if depth == 0:
			return (self.e2(), x, y)

		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if (time.time() - start) > t:
							self.current_state[i][j] = '.'
							depth = 0
							return (value, x, y)
						(v, _, _) = self.minimax(depth-1, start, t, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if (time.time() - start) > t:
							self.current_state[i][j] = '.'
							depth = 0
							return (value, x, y)
						(v, _, _) = self.minimax(depth-1, start, t, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def accept_parameters(self):
		n = int(input('the size of the board: '))
		self.initialize_game(n)
		b = int(input('the number of blocs: '))
		for i in range(b):
			bpx = int(input('enter x coordinate for bloc {}: '.format(i+1)))
			bpy = int(input('enter y coordinate for bloc {}: '.format(i+1)))
			self.current_state[bpx][bpy] = '-'
		s = int(input('the winning line-up size:'))
		d1 = int(input('the maximum depth of the adversarial search for player 1: '))
		d2 = int(input('the maximum depth of the adversarial search for player 2: '))
		t = float(input('the maximum allowed time (in seconds) for your program to return a move: '))
		a = input("minimax (FALSE) or alphabeta (TRUE)?")
		# if a == "TRUE":
		# 	a = True
		# if a == "FALSE":
		# 	a = False
		mode = input('which play mode (H-H, AI-AI, AI-H or H-AI)? ')
		return n, s, d1, d2, t, a, mode

	def alphabeta(self, d, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 1000
		if max:
			value = -1000
		x = None
		y = None
		depth = d

		if depth == 0:
			return (self.e1(), x, y)

		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(depth-1, alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(depth-1, alpha, beta, max=True)
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
		global s
		# self.initialize_game()
		n, s, d1, d2, t, a, mode = self.accept_parameters()

		if mode =='AI-AI':
			player_x = self.AI
			player_o = self.AI
		elif mode == 'AI-H':
			player_x = self.AI
			player_o = self.HUMAN
		elif mode == 'H-AI':
			player_x = self.HUMAN
			player_o = self.AI
		else:
			player_x = self.HUMAN
			player_o = self.HUMAN

		if a == 'TRUE':
			algo = self.ALPHABETA
		else:
			algo = self.MINIMAX

		# if algo == None:
		# 	algo = self.ALPHABETA
		# if player_x == None:
		# 	player_x = self.HUMAN
		# if player_o == None:
		# 	player_o = self.HUMAN
		while True:
			print("***************************")
			self.draw_board()
			print("***************************")
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(d1, start, t, max=False)
				else:
					(_, x, y) = self.minimax(d2, start, t, max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(d1, max=False)
				else:
					(m, x, y) = self.alphabeta(d2, max=True)
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
	g.play(algo=Game.MINIMAX)

if __name__ == "__main__":
	main()