import numpy as np
current_state = np.array([[".", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]])

def is_free(x, y):
    global turn
    if current_state[x % current_state.shape[0],y % current_state.shape[1]] == " " or current_state[x % current_state.shape[0],y % current_state.shape[1]] == turn:
        return True
    return False

def check_horizontal(x, y):
    global points
    original_y = y
    cons_pieces = 0
    while ((y-1) % current_state.shape[1]) != original_y:
        if is_free(x, y-1):
            cons_pieces += 1  
        y -= 1
    if cons_pieces+1 >= s:
        points += 1
#     print("horizontal point")
    
def check_vertical(x, y):
    global points
    original_x = x
    cons_pieces = 0
    while ((x-1) % current_state.shape[0]) != original_x:
        if is_free(x-1, y):
            cons_pieces += 1  
        x -= 1
    if cons_pieces+1 >= s:
        points += 1
#     print("vertical point")
    
def check_diagonal(x, y):
    global s
    global points
    cons_pieces = 0
    original_x = x
    original_y = y
    
    while (x+1) < current_state.shape[0] and (x+1) >= 0 and (y-1) < current_state.shape[1] and (y-1) >= 0:
        if is_free(x+1, y-1):
            cons_pieces += 1
        x += 1
        y -= 1

    x = original_x
    y = original_y
    
    while (x-1) < current_state.shape[0] and (x-1) >= 0 and (y+1) < current_state.shape[1] and (y+1) >= 0:
        if is_free(x-1, y+1):
            cons_pieces += 1
        x -= 1
        y += 1
    
    if cons_pieces+1 >= s:
        points += 1
        
    cons_pieces = 0
    x = original_x
    y = original_y
    
    while (x-1) < current_state.shape[0] and (x-1) >= 0 and (y-1) < current_state.shape[1] and (y-1) >= 0:
        if is_free(x-1, y-1):
            cons_pieces += 1
        x -= 1
        y -= 1

    x = original_x
    y = original_y
    
    while (x+1) < current_state.shape[0] and (x+1) >= 0 and (y+1) < current_state.shape[1] and (y+1) >= 0:
        if is_free(x+1, y+1):
            cons_pieces += 1
        x += 1
        y += 1
        
    if cons_pieces+1 >= s:
        points += 1
#     print("diagonal point")
    
def pick_move():
    global points
    best_x = -1
    best_y = -1
    best_h = -1
    for i in range(0, n):
        for j in range(0, n):
            if current_state[i][j] == " ":
#                 print("running h(",i,",",j,")...")
#                 current_state[i][j] = turn
                h = run_heuristic(i,j)
                points = 0
#                 print("h(",i,",",j,"): ",h)
                if h > best_h:
                    best_h = h
                    best_x = i
                    best_y = j
    return best_x, best_y
                

def run_heuristic(x, y):
    check_horizontal(x, y)
#     print("points: ",points)
    check_vertical(x, y)
#     print("points: ",points)
    check_diagonal(x, y)
#     print("points: ",points)
    return points

def is_end():
    # Vertical win
    for j in range(0, n):
        cons_pieces = 0
        for i in range(0, n):
            if current_state[i][j] != "." and (i+1) < n:
                if current_state[i,j] == current_state[i+1,j]:
                    cons_pieces += 1
            if cons_pieces+1 >= s:
                return current_state[i,j]
    # Horizontal win
    for i in range(0, n):
        cons_pieces = 0
        for j in range(0, n):
            if current_state[i][j] != "." and (j+1) < n:
                if current_state[i,j] == current_state[i,j+1]:
                    cons_pieces += 1
            if cons_pieces+1 >= s:
                return current_state[i,j]
    # Diagonal win
    for i in range(0, n):
        for j in range(0, n):
            cons_pieces = 0
            if current_state[i][j] != ".":
                x = i
                y = j
                while (x+1) < current_state.shape[0] and (x+1) >= 0 and (y-1) < current_state.shape[1] and (y-1) >= 0:
                    if current_state[i,j] == current_state[i+1,j-1]:
                        cons_pieces += 1
                    x += 1
                    y -= 1
                x = i
                y = j
                while (x-1) < current_state.shape[0] and (x-1) >= 0 and (y+1) < current_state.shape[1] and (y+1) >= 0:
                    if is_free(x-1, y+1):
                        cons_pieces += 1
                    x -= 1
                    y += 1
                    
                if cons_pieces+1 >= s:
                    return current_state[i,j]
                
                x = i
                y = j
                cons_pieces = 0
                
                while (x-1) < current_state.shape[0] and (x-1) >= 0 and (y-1) < current_state.shape[1] and (y-1) >= 0:
                    if is_free(x-1, y-1):
                        cons_pieces += 1
                    x -= 1
                    y -= 1

                x = i
                y = j

                while (x+1) < current_state.shape[0] and (x+1) >= 0 and (y+1) < current_state.shape[1] and (y+1) >= 0:
                    if is_free(x+1, y+1):
                        cons_pieces += 1
                x += 1
                y += 1
                
                if cons_pieces+1 >= s:
                    return current_state[i,j]
                
# Is whole board full?          
    for i in range(0, n):
        for j in range(0, n):
            # There's an empty field, we continue the game
            if (current_state[i][j] == ' '):
                return None
    # It's a tie!
    return '.'
    
def check_end():
    result = is_end()
    # Printing the appropriate message if the game has ended
    if result != None:
        if result == 'x':
            print('The winner is x!')
            return True
        elif result == 'o':
            print('The winner is o!')
            return True
        elif result == '.':
            print("It's a tie!")
            return True
    return False
    
turn = 'x'
points = 0
s = 3
n = 4

while True:
    print(current_state)
    if check_end():
        break
    x, y = pick_move()
    print("the best move for ",turn," is (",x,",",y,")")
    current_state[x][y] = turn

    if turn == 'x':
        turn = 'o'
    else:
        turn = 'x'