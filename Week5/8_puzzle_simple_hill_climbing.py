import copy

start = [[1, 2, 3],
         [4, 0, 6],
         [7, 5, 8]]

goal  = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 0]]

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

def simple_hill_climbing(start_state, goal_state):
    current_state = copy.deepcopy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    path = []
    while True:
        if states_equal(current_state, goal_state):
            return path, current_state, "Goal!"
        x, y = tim_o_trong(current_state)
        moves = p_moves(x, y)
        found_better = False
        for action in moves:
            next_state = copy.deepcopy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            next_h = manhattan_distance(next_state, goal_state)
            if next_h < current_h:
                current_state = next_state
                current_h = next_h
                path.append(action)
                found_better = True
                break 
        if not found_better:
            return path, current_state, "Không giải được!"


if __name__ == "__main__":
    result_path, final_state, status = simple_hill_climbing(start, goal)
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
    print(f"{status}")