import copy
import random
import math

start = [[2, 8, 3],
         [1, 6, 4],
         [7, 0, 5]]

goal  = [[1, 2, 3],
         [8, 0, 4],
         [7, 6, 5]]

def tim_o_trong(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def p_moves(x, y):
    moves = []
    if y > 0: 
        moves.append('L')
    if y < 2: 
        moves.append('R')
    if x > 0: 
        moves.append('U')
    if x < 2: 
        moves.append('D')
    return moves

def move(x, y, action):
    if action == 'D': 
        x += 1
    elif action == 'U': 
        x -= 1
    elif action == 'R': 
        y += 1
    elif action == 'L': 
        y -= 1
    return x, y

def states_equal(a, b):
    for i in range(3):
        for j in range(3):
            if a[i][j] != b[i][j]:
                return False
    return True

def manhattan_distance(state, goal_state):
    distance = 0
    goal_positions = {}
    for i in range(3):
        for j in range(3):
            val = goal_state[i][j]
            if val != 0:
                goal_positions[val] = (i, j)
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = goal_positions[val]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def simulated_annealing(start_state, goal_state, T0=1000, Tmin=0.1, alpha=0.95):
    current_state = copy.deepcopy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    T = T0
    path = []
    while T > Tmin:
        if states_equal(current_state, goal_state):
            return path, current_state, "Goal!"
        x, y = tim_o_trong(current_state)
        moves = p_moves(x, y)
        action = random.choice(moves)
        nx, ny = move(x, y, action)
        next_state = copy.deepcopy(current_state)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        next_h = manhattan_distance(next_state, goal_state)
        delta = next_h - current_h
        if delta < 0:
            current_state = next_state
            current_h = next_h
            path.append(action)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_state = next_state
                current_h = next_h
                path.append(action)
        T = alpha * T
    return path, current_state, "không tìm được goal!"

if __name__ == "__main__":
    result_path, final_state, status = simulated_annealing(start, goal)
    print("Trạng thái ban đầu:")
    for row in start:
        print(row)
    print(f"h(n): {manhattan_distance(start, goal)}\n")
    if result_path:
        current_state = copy.deepcopy(start)
        for action in result_path:
            x, y = tim_o_trong(current_state)
            nx, ny = move(x, y, action)
            current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
            h_val = manhattan_distance(current_state, goal)
            print(f"Action: {action}")
            print(f"h(n): {h_val}")
            for row in current_state:
                print(row)
            print()
    print(f"Trạng thái kết thúc: {status}")