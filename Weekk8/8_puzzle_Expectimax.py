import copy
import math

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

def get_result(state, action):
    new_state = copy.deepcopy(state)
    x, y = tim_o_trong(new_state)
    nx, ny = move(x, y, action)
    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state

def utility(state):
    if states_equal(state, goal):
        return 1000 
    return -manhattan_distance(state, goal)

def is_terminal(state, depth):
    return states_equal(state, goal) or depth == 0

def expectimax_search(state, depth):
    value, best_move = max_value(state, depth)
    return best_move

def max_value(state, depth):
    if is_terminal(state, depth):
        return utility(state), None
    v = -math.inf
    best_move = None
    x, y = tim_o_trong(state)
    for action in p_moves(x, y):
        next_state = get_result(state, action)
        v2, _ = exp_value(next_state, depth - 1)
        if v2 > v:
            v = v2
            best_move = action 
    return v, best_move

def exp_value(state, depth):
    if is_terminal(state, depth):
        return utility(state), None
    v = 0
    x, y = tim_o_trong(state)
    moves = p_moves(x, y)
    probability = 1.0 / len(moves)
    for action in moves:
        next_state = get_result(state, action)
        v2, _ = max_value(next_state, depth - 1)
        v += probability * v2
    return v, None

if __name__ == "__main__":
    current_state = copy.deepcopy(start)
    print("TRẠNG THÁI BAN ĐẦU:")
    for row in current_state:
        print(row)
    print(f"h(n) ban đầu: {manhattan_distance(start, goal)}")
    depth_limit = 4
    step = 0
    previous_action = None 
    print(f"\nBẮT ĐẦU TÌM ĐƯỜNG VỚI EXPECTIMAX (DEPTH = {depth_limit})")
    while not states_equal(current_state, goal):
        step += 1
        print(f"\nBƯỚC {step}")
        best_move = None
        max_v = -math.inf 
        x, y = tim_o_trong(current_state)
        for action in p_moves(x, y):
            if previous_action == 'U' and action == 'D': continue
            if previous_action == 'D' and action == 'U': continue
            if previous_action == 'L' and action == 'R': continue
            if previous_action == 'R' and action == 'L': continue
            next_state = get_result(current_state, action)
            v, _ = exp_value(next_state, depth_limit - 1)
            if v > max_v:
                max_v = v
                best_move = action      
        if best_move is None:
            best_move = expectimax_search(current_state, depth_limit)
        print(f"MAX: {best_move} (Đánh giá điểm kỳ vọng: {max_v:.2f})")
        current_state = get_result(current_state, best_move)
        for row in current_state:
            print(row)  
        previous_action = best_move
        if step >= 50: 
            print("\nĐã đạt giới hạn 50 bước.")
            break  
    if states_equal(current_state, goal):
        print(f"\nĐÃ TÌM THẤY ĐÍCH TRONG {step} BƯỚC!")