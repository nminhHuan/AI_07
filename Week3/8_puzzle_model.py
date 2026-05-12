import random

def p_moves(x, y):
    moves = []
    if x > 0: moves.append('U')
    if x < 2: moves.append('D')
    if y > 0: moves.append('L')
    if y < 2: moves.append('R')
    return moves

def move(x, y, action):
    if action == 'U':
        x -= 1
    elif action == 'D':
        x += 1
    elif action == 'L':
        y -= 1
    elif action == 'R':
        y += 1
    return x, y

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def print_state(state):
    for row in state:
        print(" ".join(map(str, row)))
    print()

def opposite(action):
    return {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}.get(action, None)

if __name__ == "__main__":
    state = []
    for i in range(3):
        state.append(list(map(int, input().split())))
    target = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    print("Trang thai ban dau:")
    print_state(state)
    prev_action = None
    step = 0
    MAX_STEP = 10000
    while step < MAX_STEP:
        if state == target:
            print(f"Da dat target sau {step} buoc!")
            break
        x, y = find_blank(state)
        moves = p_moves(x, y)
        if prev_action:
            opp = opposite(prev_action)
            filtered = [m for m in moves if m != opp]
            moves = filtered if filtered else moves
        action = random.choice(moves)
        new_x, new_y = move(x, y, action)
        state[x][y], state[new_x][new_y] = state[new_x][new_y], state[x][y]
        prev_action = action
        step += 1
        print(f"Step {step} - Action: {action}")
        print_state(state)
    else:
        print(f"Qua {MAX_STEP} buoc, bi ket!")