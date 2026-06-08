import copy
import heapq  

start_states = [
    [[2, 8, 3],
     [1, 6, 4],
     [7, 0, 5]],

    [[2, 8, 3],
     [1, 6, 4],
     [0, 7, 5]],
]

goal = [[1, 2, 3],
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

def apply_action(state, action):
    x, y = tim_o_trong(state)
    if action not in p_moves(x, y):
        return copy.deepcopy(state)
    nx, ny = move(x, y, action)
    new_state = copy.deepcopy(state)
    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state

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

def h_belief(belief, goal_state):
    return sum(manhattan_distance(s, goal_state) for s in belief)

def belief_to_tuple(belief):
    return tuple(tuple(tuple(row) for row in s) for s in belief)

def greedy_belief_state_search(start_belief, goal_state):
    frontier = []
    in_frontier = set() 
    counter = 0        
    start_tuple = belief_to_tuple(start_belief)
    h_start = h_belief(start_belief, goal_state)
    heapq.heappush(frontier, (h_start, counter, start_belief))
    in_frontier.add(start_tuple)
    counter += 1
    reached = set()
    parent = {start_tuple: (None, None)}
    while frontier:
        h_n, _, current_belief = heapq.heappop(frontier)
        current_tuple = belief_to_tuple(current_belief)
        in_frontier.discard(current_tuple) 
        if all(states_equal(s, goal_state) for s in current_belief):
            path = []
            node = current_tuple
            while parent[node][0] is not None:
                path.append(parent[node][1]) 
                node = parent[node][0]     
            path.reverse()
            return path, current_belief, "Goal!"
        reached.add(current_tuple)
        all_act = set()
        for s in current_belief:
            x, y = tim_o_trong(s)
            for a in p_moves(x, y):
                all_act.add(a)    
        for action in ['L', 'R', 'U', 'D']:
            if action not in all_act:
                continue
            child_belief = [apply_action(s, action) for s in current_belief]
            child_tuple = belief_to_tuple(child_belief)
            if child_tuple not in in_frontier and child_tuple not in reached:
                parent[child_tuple] = (current_tuple, action)
                h_m = h_belief(child_belief, goal_state)
                heapq.heappush(frontier, (h_m, counter, child_belief))
                in_frontier.add(child_tuple)
                counter += 1
    return [], start_belief, "Thất bại"

if __name__ == "__main__":
    result_path, final_belief, status = greedy_belief_state_search(start_states, goal)
    if status == "Goal!":
        current_belief = copy.deepcopy(start_states)
        print("Trạng thái ban đầu:")
        for idx, s in enumerate(current_belief):
            print(f"  state {idx+1} [h={manhattan_distance(s, goal)}]:")
            for row in s:
                print(f"    {row}")        
        for action in result_path:
            current_belief = [apply_action(s, action) for s in current_belief]
            print(f"action: {action}")
            for idx, s in enumerate(current_belief):
                goal_check = "GOAL" if states_equal(s, goal) else f"h={manhattan_distance(s, goal)}"
                print(f"  state {idx+1} [{goal_check}]:")
                for row in s:
                    print(f"    {row}")
    print(f"{status}")
    print(f"Path: {result_path}")