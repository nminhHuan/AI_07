import copy
import sys

sys.setrecursionlimit(50000)

start = [[1, 2, 3],
         [4, 0, 5],
         [7, 8, 6]]

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

def backtracking_search(start_state, goal_state):
    visited = set()
    visited.add(state_to_tuple(start_state))
    return recursive_backtracking(start_state, goal_state, [], visited)

def recursive_backtracking(current_state, goal_state, path, visited):
    if states_equal(current_state, goal_state):
        return list(path) 
    x, y = tim_o_trong(current_state)
    moves = p_moves(x, y)
    for action in moves:
        nx, ny = move(x, y, action)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        child_tuple = state_to_tuple(current_state)
        if child_tuple not in visited:
            visited.add(child_tuple)
            path.append(action)
            result = recursive_backtracking(current_state, goal_state, path, visited)
            if result is not None:
                return result
            path.pop()
            visited.remove(child_tuple) 
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
    return None

if __name__ == "__main__":
    result_path = backtracking_search(copy.deepcopy(start), goal)
    if result_path is not None:
        print("Trạng thái ban đầu:")
        for row in start:
            print(row)
        print()
        current_state = copy.deepcopy(start)
        for action in result_path:
            x, y = tim_o_trong(current_state)
            nx, ny = move(x, y, action)
            current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
            print(f"Action: {action}")
            for row in current_state:
                print(row)
            print()
        print(f"step: {len(result_path)}")
        print("GOAL!")
    else:
        print("Không tìm thấy lời giải!")