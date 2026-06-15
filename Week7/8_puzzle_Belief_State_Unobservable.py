#Môi trường không quan sát được (DFS)
import copy

start_states = [
    [[2, 8, 3],
     [1, 6, 4],
     [7, 0, 5]],

    [[8, 7, 6],
     [1, 0, 5],
     [2, 3, 4]]
]

goal_states = [
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 0]],

    [[1, 2, 3],
     [8, 0, 4],
     [7, 6, 5]],

    [[8, 7, 6],
     [1, 0, 5],
     [2, 3, 4]]
]

def tim_o_trong(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def p_moves(x, y):
    moves = []
    if x < 2: 
        moves.append('D')
    if x > 0: 
        moves.append('U')
    if y < 2: 
        moves.append('R')
    if y > 0: 
        moves.append('L')
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

def apply_action(state, action):
    x, y = tim_o_trong(state)
    if action not in p_moves(x, y):
        return copy.deepcopy(state)
    nx, ny = move(x, y, action)
    new_state = copy.deepcopy(state)
    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state

def belief_to_tuple(belief):
    return tuple(sorted(tuple(tuple(row) for row in s) for s in belief))

def is_belief_goal(belief, bg_set):
    for g in bg_set:
        if all(states_equal(s, g) for s in belief):
            return True
    return False

def print_belief_state(belief):
    for idx, s in enumerate(belief):
        print(f"  State {idx+1}:")
        for row in s:
            print(f"    {row}")
    print()

def dfs_belief(start_belief, bg_set):
    if is_belief_goal(start_belief, bg_set):
        return 0
    frontier = []
    frontier.append((start_belief, 0, None))
    explored = set() 
    while frontier:
        node, cost, action_taken = frontier.pop()
        node_tuple = belief_to_tuple(node)
        if node_tuple in explored:
            continue
        explored.add(node_tuple)
        if action_taken is not None:
            print("Action:", action_taken)
            print("Cost:", cost)
            print_belief_state(node)
        if is_belief_goal(node, bg_set):
            return cost
        all_act = set()
        for s in node:
            x, y = tim_o_trong(s)
            for a in p_moves(x, y):
                all_act.add(a)
        for action in ['D', 'R', 'L', 'U']:
            if action not in all_act:
                continue
            child = [apply_action(s, action) for s in node]
            child_tuple = belief_to_tuple(child)
            frontier_states = [belief_to_tuple(s) for s, c, a in frontier]
            if child_tuple not in explored and child_tuple not in frontier_states:
                frontier.append((child, cost + 1, action))
    return None

print("trạng thái ban đầu")
print_belief_state(start_states)
print("duyệt DFS")
cost = dfs_belief(start_states, goal_states)
print("kết quả")
if cost is not None:
    print("Total Cost:", cost)
else:
    print("Không giải được")