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

def forward_checking(state, x, y, domain, visited):
    valid_domain = []
    for action in domain:
        nx, ny = move(x, y, action)
        state[x][y], state[nx][ny] = state[nx][ny], state[x][y]
        child_tuple = state_to_tuple(state)
        state[x][y], state[nx][ny] = state[nx][ny], state[x][y]
        if child_tuple not in visited:
            valid_domain.append(action)
    return valid_domain  

def forward_check(current_state, goal_state, path, visited):
    if states_equal(current_state, goal_state):
        return list(path)
    x, y = tim_o_trong(current_state)
    domain = p_moves(x, y)
    domain = forward_checking(current_state, x, y, domain, visited)
    for action in domain:
        nx, ny = move(x, y, action)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        child_tuple = state_to_tuple(current_state)
        visited.add(child_tuple)
        path.append(action)
        result = forward_check(current_state, goal_state, path, visited)
        if result is not None:
            return result
        path.pop()
        visited.remove(child_tuple)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
    return None

def forward_checking_search(start_state, goal_state):
    visited = set()
    visited.add(state_to_tuple(start_state))
    return forward_check(start_state, goal_state, [], visited)

if __name__ == "__main__":
    result_path = forward_checking_search(copy.deepcopy(start), goal)
    if result_path is not None:
        print("Trang thai ban dau:")
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
        print("Khong tim thay loi giai!")