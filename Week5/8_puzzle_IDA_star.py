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

def state_in_list(state, lst):
    for s in lst:
        if states_equal(s, state):
            return True
    return False

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

def f_limited_search(start_state, goal_state, f_limit):
    h_start = manhattan_distance(start_state, goal_state)
    f_start = 0 + h_start  
    frontier = [[start_state, [], 0, [copy.deepcopy(start_state)]]]
    result_status = "failure"
    min_f_exceeded = float('inf')   
    while frontier:
        node_state, path, g, ancestors = frontier.pop()
        h = manhattan_distance(node_state, goal_state)
        f = g + h
        if states_equal(node_state, goal_state):
            return path, "found", f
        if f > f_limit:
            min_f_exceeded = min(min_f_exceeded, f)
            result_status = "cutoff"
            continue  
        x, y = tim_o_trong(node_state)
        for action in p_moves(x, y):
            child_state = copy.deepcopy(node_state) 
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            if not state_in_list(child_state, ancestors):
                new_ancestors = copy.deepcopy(ancestors)
                new_ancestors.append(child_state)
                frontier.append([child_state, path + [action], g + 1, new_ancestors])
    return None, result_status, min_f_exceeded

def ida_star_search(start_state, goal_state):
    if states_equal(start_state, goal_state):
        return [], 0
    threshold = manhattan_distance(start_state, goal_state)
    while True:
        result_path, result_status, val = f_limited_search(start_state, goal_state, threshold)
        if result_status == "found":
            return result_path, threshold
        if result_status == "failure":
            return None, -1
        if val == float('inf'):         
            return None, -1
        threshold = val

if __name__ == "__main__":
    result_path, final_threshold = ida_star_search(start, goal)
    if result_path is not None:
        print("Trạng thái ban đầu:")
        for row in start:
            print(row)
        print()
        current_state = copy.deepcopy(start)
        g_val = 0
        for action in result_path:
            x, y = tim_o_trong(current_state)
            nx, ny = move(x, y, action)
            current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
            g_val += 1
            h_val = manhattan_distance(current_state, goal)
            f_val = g_val + h_val
            print(f"Action: {action}")
            print(f"g(n): {g_val} | h(n): {h_val} | f(n): {f_val}")
            for row in current_state:
                print(row)
        print(f"Goal! (f* = {final_threshold})")
    else:
        print("Không tìm thấy lời giải!")