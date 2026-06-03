import copy
import random

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

def random_state_from_start(start_state, steps=5):
    state = copy.deepcopy(start_state)
    path = []
    for _ in range(steps):
        x, y = tim_o_trong(state)
        action = random.choice(p_moves(x, y))
        nx, ny = move(x, y, action)
        state[x][y], state[nx][ny] = state[nx][ny], state[x][y]
        path.append(action)
    return state, path

def local_beam_search(start_state, goal_state, k=4):
    current_state_set = []
    visited = set()
    for i in range(k):
        board, init_path = random_state_from_start(start_state)
        board_str = str(board)
        if board_str not in visited:
            visited.add(board_str)
        current_state_set.append({
            'board': board,
            'path': init_path,
            'h': manhattan_distance(board, goal_state)
        })
    while True:
        neighbor_states = []
        for state_info in current_state_set:
            current_board = state_info['board']
            current_path  = state_info['path']
            x, y = tim_o_trong(current_board)
            moves = p_moves(x, y)
            for action in moves:
                next_board = copy.deepcopy(current_board)
                nx, ny = move(x, y, action)
                next_board[x][y], next_board[nx][ny] = next_board[nx][ny], next_board[x][y]
                board_str = str(next_board)
                if board_str not in visited:
                    visited.add(board_str)
                    neighbor_states.append({
                        'board': next_board,
                        'path': current_path + [action],
                        'h': manhattan_distance(next_board, goal_state)
                    })
        for neighbor in neighbor_states:
            if states_equal(neighbor['board'], goal_state):
                return neighbor['path'], neighbor['board'], "Goal!"
        if len(neighbor_states) == 0:
            return None, None, "Thất bại!"
        neighbor_states.sort(key=lambda item: item['h'])
        current_state_set = neighbor_states[:k]

if __name__ == "__main__":
    k_beam = 3
    print(f"k = {k_beam}")
    result_path, final_state, status = local_beam_search(start, goal, k=k_beam)
    print("Trạng thái ban đầu:")
    for row in start:
        print(row)
    print(f"h(n) ban đầu: {manhattan_distance(start, goal)}\n")
    if result_path is not None:
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
    if result_path is not None:
        print(f"Số bước di chuyển: {len(result_path)}")
    else:
        print(status)