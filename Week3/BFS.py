from collections import deque
import random
import copy

goal = [[1,2,3],
        [8,0,4],
        [7,6,5]]

state = [[2,8,3],
         [1,6,4],
         [7,0,5]]

def tim_o_trong(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def p_moves(x,y):
    moves=[]
    if x < 2:
        moves.append('D')
    if x > 0:
        moves.append('U')
    if y < 2:
        moves.append('R')
    if y > 0:
        moves.append('L')
    return moves

def move(x,y,action):
    if action == 'D':
        x += 1
    elif action == 'U':
        x -= 1
    elif action == 'R':
        y += 1
    elif action == 'L':
        y -= 1
    return x,y

def print_board(board):
    for row in board:
        print(row)
    print()

def bfs(state,goal):
    if state == goal:
        return 0
    frontier = deque()
    frontier.append((state,0))
    explored = []
    
    while frontier:
        node, cost = frontier.popleft()
        explored.append(node)
        x,y = tim_o_trong(node)
        moves = p_moves(x,y)
        random.shuffle(moves)
        for action in moves:
            child = copy.deepcopy(node)
            nx, ny = move(x,y,action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            print("Action:",action)
            print("Cost:",cost+1)
            print_board(child)
            frontier_states = []
            for s, c in frontier:
                frontier_states.append(s)
            if child not in explored and child not in frontier_states:
                if child == goal:
                    return cost + 1
                frontier.append((child,cost+1))
    return None

print("trạng thái ban đầu")
print_board(state)

cost = bfs(state,goal)

if cost is not None:
    print("Total Cost:",cost)

else:
    print("Không giải được")