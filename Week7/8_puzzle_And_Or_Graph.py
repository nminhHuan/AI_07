import copy
import sys
sys.setrecursionlimit(100000)

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
    return all(a[i][j] == b[i][j] for i in range(3) for j in range(3))

def state_to_tuple(state):
    return tuple(state[i][j] for i in range(3) for j in range(3))

def get_result_states(state, action):
    x, y = tim_o_trong(state)
    nx, ny = move(x, y, action)
    next_state = copy.deepcopy(state)
    next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
    return [next_state]

FAILURE = "FAILURE"

def OR_SEARCH(state, goal_state, path, depth_limit):
    if states_equal(state, goal_state):
        return []
    state_key = state_to_tuple(state)
    if state_key in path:
        return FAILURE
    if depth_limit == 0:
        return FAILURE
    x, y = tim_o_trong(state)
    for action in p_moves(x, y):
        result_states = get_result_states(state, action)
        plan = AND_SEARCH(result_states, goal_state, path | {state_key}, depth_limit - 1)
        if plan is not FAILURE:
            return [action, plan]
    return FAILURE

def AND_SEARCH(states, goal_state, path, depth_limit):
    plans = {}
    for s in states:
        plan_s = OR_SEARCH(s, goal_state, path, depth_limit)
        if plan_s is FAILURE:
            return FAILURE
        plans[state_to_tuple(s)] = plan_s
    return plans

def AND_OR_GRAPH_SEARCH(initial_state, goal_state, max_depth=30):
    for depth in range(1, max_depth + 1):
        plan = OR_SEARCH(initial_state, goal_state, path=set(), depth_limit=depth)
        if plan is not FAILURE:
            return plan, depth
    return FAILURE, max_depth

def extract_action_sequence(plan):
    actions = []
    current = plan
    while current and isinstance(current, list):
        action, sub_plans = current[0], current[1]
        actions.append(action)
        if not sub_plans:
            break
        current = next(iter(sub_plans.values()))
    return actions

if __name__ == "__main__":
    print("Trạng thái ban đầu:")
    for row in start:
        print(row)
    print()
    plan, depth_used = AND_OR_GRAPH_SEARCH(start, goal, max_depth=30)
    if plan is FAILURE:
        print("Không tìm được kế hoạch!")
    else:
        action_sequence = extract_action_sequence(plan)
        current_state = copy.deepcopy(start)
        for action in action_sequence:
            x, y = tim_o_trong(current_state)
            nx, ny = move(x, y, action)
            current_state[x][y], current_state[nx][ny] = (
                current_state[nx][ny], current_state[x][y]
            )
            print(f"Action: {action}")
            for row in current_state:
                print(row)
            print()
        print("Trạng thái kết thúc: Goal!")
        print(f"Tổng số bước: {len(action_sequence)}")