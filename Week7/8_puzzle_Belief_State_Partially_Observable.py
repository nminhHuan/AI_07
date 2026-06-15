#Môi trường nhìn thấy 1 phần (DFS)
import copy

start_states = [
    [[1, 2, 3],
     [4, 0, 6],
     [7, 5, 8]],

    [[1, 2, 3],
     [4, 5, 6],
     [0, 7, 8]]
]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


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


def apply_action(state, action):
    x, y = tim_o_trong(state)
    if action not in p_moves(x, y):
        return copy.deepcopy(state)
    nx, ny = x, y
    if action == 'D': nx += 1
    elif action == 'U': nx -= 1
    elif action == 'R': ny += 1
    elif action == 'L': ny -= 1
    new_state = copy.deepcopy(state)
    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state


def belief_to_tuple(belief):
    unique_states = []
    for s in belief:
        if s not in unique_states:
            unique_states.append(s)
    return tuple(sorted(tuple(tuple(row) for row in s) for s in unique_states))

def is_belief_goal(belief, goal_state):
    for s in belief:
        if s != goal_state:
            return False
    return True

def print_belief_state(belief):
    for idx, s in enumerate(belief):
        print(f"  Trạng thái {idx+1}:")
        for row in s:
            print(f"    {row}")

def dfs_belief(start_node, goal_state):
    frontier = [(start_node, [])]
    explored = set()
    while frontier:
        node, path = frontier.pop() 
        node_tuple = belief_to_tuple(node)
        if node_tuple in explored:
            continue
        explored.add(node_tuple)
        if path:
            print(f"action: {path[-1]} | Cost: {len(path)}")
            print_belief_state(node)
        if is_belief_goal(node, goal_state):
            return path
        for action in ['U', 'R', 'L', 'D']:
            child_belief = [apply_action(s, action) for s in node]
            child_tuple = belief_to_tuple(child_belief)
            if child_tuple not in explored:
                frontier.append((child_belief, path + [action])) 
    return None

print("Trạng thái ban đầu")
print_belief_state(start_states)
path = dfs_belief(start_states, goal_state)
print("KẾT QUẢ:")
if path is not None:
    print(f"Các bước di chuyển: {' -> '.join(path)}")
    print(f"Tổng chi phí (Cost): {len(path)}")
else:
    print("Không giải được.")