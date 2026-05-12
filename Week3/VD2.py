state = [
    [1, 3, 5],
    [4, 6, 8],
    [2, 7, 0]  # 0 la o trong
]

def simple_reflex_agent(state):
    # Buoc 1: INTERPRET-INPUT - tim o trong
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                row, col = i, j

    # Buoc 2: RULE-MATCH - chon hanh dong
    if row > 0:
        action = "UP"
    elif col > 0:
        action = "LEFT"
    elif row < 2:
        action = "DOWN"
    elif col < 2:
        action = "RIGHT"
    else:
        action = None

    # Buoc 3: Thuc hien hanh dong
    if action == "UP":
        state[row][col], state[row-1][col] = state[row-1][col], state[row][col]
    elif action == "LEFT":
        state[row][col], state[row][col-1] = state[row][col-1], state[row][col]
    elif action == "DOWN":
        state[row][col], state[row+1][col] = state[row+1][col], state[row][col]
    elif action == "RIGHT":
        state[row][col], state[row][col+1] = state[row][col+1], state[row][col]

    return action, state

buoc = 0
target = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

while buoc < 50:
    buoc += 1
    action, state = simple_reflex_agent(state)
    print(f"Buoc {buoc} - Action: {action}")
    for i in state:
        print(i)
    print()
    if state == target:
        print("Da dat target!")
        break
else:
    print("Qua 50 buoc, bi ket!")