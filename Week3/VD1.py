state = [
    [1, 3, 5],
    [4, 6, 8],
    [2, 7, 0]  # 0 la o trong
]

def simple_reflex_agent(a):
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
    # Buoc 3: Thuc hien hanh dong
    if action == "UP":
        state[row][col], state[row-1][col] = state[row-1][col], state[row][col]
    elif action == "LEFT":
        state[row][col], state[row][col-1] = state[row][col-1], state[row][col]

    return action, state

action, state = simple_reflex_agent(state)
print("Action:",action)
for i in state:
    print(i)