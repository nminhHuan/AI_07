import copy
import heapq

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

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

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

def a_star_search(start_state, goal_state):
    frontier = []
    counter = 0
    start_tuple = state_to_tuple(start_state)
    g_start = 0
    h_start = manhattan_distance(start_state, goal_state)
    f_start = g_start + h_start
    parent = {start_tuple: (None, None)}
    heapq.heappush(frontier, (f_start, counter, start_state, g_start))
    counter += 1
    frontier_states = {start_tuple: g_start}
    reached = {}
    while frontier:
        f_n, _, current_state, g_n = heapq.heappop(frontier)
        current_tuple = state_to_tuple(current_state)
        if current_tuple in reached and reached[current_tuple] <= g_n:
            continue
        if states_equal(current_state, goal_state):
            path = []
            node = current_tuple
            while parent[node][0] is not None:
                path.append(parent[node][1])
                node = parent[node][0]
            path.reverse()
            return path
        if current_tuple in frontier_states:
            del frontier_states[current_tuple]
        reached[current_tuple] = g_n
        x, y = tim_o_trong(current_state)
        for action in p_moves(x, y):
            child_state = [row[:] for row in current_state]
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            child_tuple = state_to_tuple(child_state)
            g_new = g_n + 1
            if child_tuple in reached:
                if g_new >= reached[child_tuple]:
                    continue  
                else:
                    del reached[child_tuple]
                    parent[child_tuple] = (current_tuple, action)  
                    frontier_states[child_tuple] = g_new
                    h_m = manhattan_distance(child_state, goal_state)
                    heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                    counter += 1
                continue
            if child_tuple in frontier_states:
                if g_new < frontier_states[child_tuple]:
                    frontier_states[child_tuple] = g_new
                    parent[child_tuple] = (current_tuple, action)  
                    h_m = manhattan_distance(child_state, goal_state)
                    heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                    counter += 1
            else:
                frontier_states[child_tuple] = g_new
                parent[child_tuple] = (current_tuple, action)  
                h_m = manhattan_distance(child_state, goal_state)
                heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                counter += 1
    return None

if __name__ == "__main__":
    result_path = a_star_search(start, goal)
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
            print("-" * 15)
        print("Goal!")
    else:
        print("Không tìm thấy lời giải cho trạng thái này!")