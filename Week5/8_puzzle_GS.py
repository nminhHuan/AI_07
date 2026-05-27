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

def greedy_search(start_state, goal_state):
    frontier = []  
    counter = 0 
    h_start = manhattan_distance(start_state, goal_state)
    heapq.heappush(frontier, (h_start, counter, start_state, []))
    counter += 1
    frontier_states = {state_to_tuple(start_state)} 
    reached = set()
    while frontier:
        h_n, _, current_state, path = heapq.heappop(frontier)
        current_tuple = state_to_tuple(current_state)
        if current_tuple in frontier_states:
            frontier_states.remove(current_tuple)
        if states_equal(current_state, goal_state):
            return path
        reached.add(current_tuple)
        x, y = tim_o_trong(current_state)
        moves = p_moves(x, y)
        for action in moves:
            child_state = copy.deepcopy(current_state)
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            child_tuple = state_to_tuple(child_state)
            if child_tuple not in frontier_states and child_tuple not in reached:
                h_m = manhattan_distance(child_state, goal_state)
                heapq.heappush(frontier, (h_m, counter, child_state, path + [action]))
                counter += 1 
                frontier_states.add(child_tuple)
    return None


if __name__ == "__main__":
    result_path = greedy_search(start, goal)
    if result_path is not None:
        print("trạng thái ban đầu")
        for row in start:
            print(row)
        print()
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
            
    else:
        print("không tìm thấy lời giải!")