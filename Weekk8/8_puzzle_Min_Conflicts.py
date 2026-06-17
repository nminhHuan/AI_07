import copy
import random

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

def count_conflicts(state, goal_state):
    conflicts = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                for gi in range(3):
                    for gj in range(3):
                        if goal_state[gi][gj] == val:
                            conflicts += abs(i - gi) + abs(j - gj)
    return conflicts

def min_conflicts_search(start_state, goal_state, max_steps=1000):
    current = copy.deepcopy(start_state)
    path = []
    for step in range(max_steps):
        if states_equal(current, goal_state):
            return path
        x, y = tim_o_trong(current)
        moves = p_moves(x, y)
        best_moves = []
        min_conflict_val = float('inf')
        for action in moves:
            nx, ny = move(x, y, action)
            neighbor = copy.deepcopy(current)
            neighbor[x][y], neighbor[nx][ny] = neighbor[nx][ny], neighbor[x][y]
            conflict_val = count_conflicts(neighbor, goal_state)
            if conflict_val < min_conflict_val:
                min_conflict_val = conflict_val
                best_moves = [(action, neighbor)]
            elif conflict_val == min_conflict_val:
                best_moves.append((action, neighbor))
        best_action, next_state = random.choice(best_moves)
        path.append(best_action)
        current = next_state    
    return None

if __name__ == "__main__":
    result_path = min_conflicts_search(copy.deepcopy(start), goal, max_steps=500)
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
        print(f"Steps: {len(result_path)}")
        print("GOAL!")
    else:
        print("Không tìm thấy lời giải!")