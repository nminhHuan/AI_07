import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import threading
from collections import deque
import heapq
import math
import sys
import copy

sys.setrecursionlimit(100000)

GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

START_STATE = [[1, 2, 3],
               [4, 0, 6],
               [7, 5, 8]]

def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def p_moves(x, y):
    moves = []
    if x > 0: 
        moves.append('U')
    if y > 0: 
        moves.append('L')
    if y < 2: 
        moves.append('R')
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

def state_to_str(state):
    return str(state)

def count_inversions(state):
    arr = []
    for row in state:
        for val in row:
            if val > 0: 
                arr.append(val)             
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def is_solvable(state):
    return count_inversions(state) % 2 == 0

def fast_copy(state):
    return [row[:] for row in state]

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

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
            if val != 0 and val != -1: 
                goal_i, goal_j = goal_positions[val]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def bfs(start_state, goal_state):
    if start_state == goal_state: return []
    frontier = deque([(start_state, [])])
    explored = set([state_to_str(start_state)])
    while frontier:
        node, path = frontier.popleft()
        if node == goal_state: return path
        x, y = find_empty_tile(node)
        for action in p_moves(x, y):
            child = fast_copy(node)
            nx, ny = move(x, y, action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            child_str = state_to_str(child)
            if child_str not in explored:
                explored.add(child_str)
                frontier.append((child, path + [action]))
    return None

def dfs(start_state, goal_state):
    if start_state == goal_state: return []
    frontier = [(start_state, [])]
    explored = set()
    while frontier:
        node, path = frontier.pop()
        node_str = state_to_str(node)
        if node == goal_state: return path
        if node_str in explored: continue
        explored.add(node_str)
        x, y = find_empty_tile(node)
        moves = p_moves(x, y)
        for action in moves:
            child = fast_copy(node)
            nx, ny = move(x, y, action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            frontier.append((child, path + [action]))
    return None

def backtracking_search(start_state, goal_state):
    working_state = fast_copy(start_state)
    visited = set()
    visited.add(state_to_tuple(working_state))
    return recursive_backtracking(working_state, goal_state, [], visited)

def recursive_backtracking(current_state, goal_state, path, visited):
    if current_state == goal_state:
        return list(path) 
    x, y = find_empty_tile(current_state)
    moves = p_moves(x, y)
    for action in moves:
        nx, ny = move(x, y, action)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        child_tuple = state_to_tuple(current_state)
        if child_tuple not in visited:
            visited.add(child_tuple)
            path.append(action)
            result = recursive_backtracking(current_state, goal_state, path, visited)
            if result is not None:
                return result
            path.pop()
            visited.remove(child_tuple) 
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
    return None

def depth_limited_search(start_state, goal_state, limit):
    frontier = [(start_state, [], 0)]
    explored_at_depth = {}
    while frontier:
        node, path, depth = frontier.pop()
        node_str = state_to_str(node)
        if node == goal_state: return path, "found"
        if depth >= limit: continue
        if node_str in explored_at_depth and explored_at_depth[node_str] <= depth:
            continue
        explored_at_depth[node_str] = depth
        x, y = find_empty_tile(node)
        for action in p_moves(x, y):
            child = fast_copy(node)
            nx, ny = move(x, y, action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            frontier.append((child, path + [action], depth + 1))
    return None, "cutoff"

def ids(start_state, goal_state):
    MAX_DEPTH = 30
    for depth in range(MAX_DEPTH + 1):
        result_path, status = depth_limited_search(start_state, goal_state, depth)
        if status == "found": return result_path
    return None

def ucs(start_state, goal_state):
    if start_state == goal_state: return []
    counter = 0 
    frontier = []
    heapq.heappush(frontier, (0, counter, start_state, []))
    explored = set()
    while frontier:
        current_cost, _, node, path = heapq.heappop(frontier)
        node_str = state_to_str(node)
        if node == goal_state: return path
        if node_str in explored: continue
        explored.add(node_str)
        x, y = find_empty_tile(node)
        for action in p_moves(x, y):
            child = fast_copy(node)
            nx, ny = move(x, y, action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            if state_to_str(child) not in explored:
                counter += 1
                new_cost = current_cost + 1
                heapq.heappush(frontier, (new_cost, counter, child, path + [action]))
    return None

def a_star_search(start_state, goal_state):
    if start_state == goal_state: return []
    frontier = []
    counter = 0
    start_tuple = state_to_tuple(start_state)
    g_start = 0
    h_start = manhattan_distance(start_state, goal_state)
    f_start = g_start + h_start
    parent = {start_tuple: (None, None)}
    heapq.heappush(frontier, (f_start, counter, start_state, g_start))
    counter += 1
    frontier_states = {start_tuple: g_start}
    reached = {}
    while frontier:
        f_n, _, current_state, g_n = heapq.heappop(frontier)
        current_tuple = state_to_tuple(current_state)
        if current_tuple in reached and reached[current_tuple] <= g_n:
            continue
        if current_state == goal_state:
            path = []
            node = current_tuple
            while parent[node][0] is not None:
                path.append(parent[node][1])
                node = parent[node][0]
            path.reverse()
            return path
        if current_tuple in frontier_states:
            del frontier_states[current_tuple]
        reached[current_tuple] = g_n
        x, y = find_empty_tile(current_state)
        for action in p_moves(x, y):
            child_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            child_tuple = state_to_tuple(child_state)
            g_new = g_n + 1
            if child_tuple in reached:
                if g_new >= reached[child_tuple]:
                    continue  
                else:
                    del reached[child_tuple]
                    parent[child_tuple] = (current_tuple, action)  
                    frontier_states[child_tuple] = g_new
                    h_m = manhattan_distance(child_state, goal_state)
                    heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                    counter += 1
                continue
            if child_tuple in frontier_states:
                if g_new < frontier_states[child_tuple]:
                    frontier_states[child_tuple] = g_new
                    parent[child_tuple] = (current_tuple, action)  
                    h_m = manhattan_distance(child_state, goal_state)
                    heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                    counter += 1
            else:
                frontier_states[child_tuple] = g_new
                parent[child_tuple] = (current_tuple, action)  
                h_m = manhattan_distance(child_state, goal_state)
                heapq.heappush(frontier, (g_new + h_m, counter, child_state, g_new))
                counter += 1
    return None

def greedy_search(start_state, goal_state):
    if start_state == goal_state: return []
    frontier = []  
    counter = 0 
    h_start = manhattan_distance(start_state, goal_state)
    heapq.heappush(frontier, (h_start, counter, start_state, []))
    counter += 1
    start_tuple = state_to_tuple(start_state)
    frontier_states = {start_tuple} 
    reached = set()
    while frontier:
        h_n, _, current_state, path = heapq.heappop(frontier)
        current_tuple = state_to_tuple(current_state)
        if current_tuple in frontier_states:
            frontier_states.remove(current_tuple)
        if current_state == goal_state:
            return path
        reached.add(current_tuple)
        x, y = find_empty_tile(current_state)
        moves = p_moves(x, y)
        for action in moves:
            child_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            child_tuple = state_to_tuple(child_state)
            if child_tuple not in frontier_states and child_tuple not in reached:
                h_m = manhattan_distance(child_state, goal_state)
                heapq.heappush(frontier, (h_m, counter, child_state, path + [action]))
                counter += 1 
                frontier_states.add(child_tuple)
    return None

def f_limited_search(start_state, goal_state, f_limit):
    h_start = manhattan_distance(start_state, goal_state)
    start_tuple = state_to_tuple(start_state)
    frontier = [(start_state, [], 0, set([start_tuple]))]
    result_status = "failure"
    min_f_exceeded = float('inf') 
    while frontier:
        node_state, path, g, ancestors = frontier.pop()
        h = manhattan_distance(node_state, goal_state)
        f = g + h
        if node_state == goal_state:
            return path, "found", f
        if f > f_limit:
            min_f_exceeded = min(min_f_exceeded, f)
            result_status = "cutoff"
            continue 
        x, y = find_empty_tile(node_state)
        for action in p_moves(x, y):
            child_state = fast_copy(node_state) 
            nx, ny = move(x, y, action)
            child_state[x][y], child_state[nx][ny] = child_state[nx][ny], child_state[x][y]
            child_tuple = state_to_tuple(child_state)
            if child_tuple not in ancestors:
                new_ancestors = ancestors.copy()
                new_ancestors.add(child_tuple)
                frontier.append((child_state, path + [action], g + 1, new_ancestors))
    return None, result_status, min_f_exceeded

def ida_star_search(start_state, goal_state):
    if start_state == goal_state: return []
    threshold = manhattan_distance(start_state, goal_state)
    while True:
        result_path, result_status, val = f_limited_search(start_state, goal_state, threshold)
        if result_status == "found":
            return result_path
        if result_status == "failure":
            return None
        if val == float('inf'):         
            return None
        threshold = val

def simple_hill_climbing(start_state, goal_state):
    current_state = fast_copy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    path = []
    while True:
        if current_state == goal_state:
            return path
        x, y = find_empty_tile(current_state)
        moves = p_moves(x, y)
        found_better = False
        for action in moves:
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            next_h = manhattan_distance(next_state, goal_state)
            if next_h < current_h:
                current_state = next_state
                current_h = next_h
                path.append(action)
                found_better = True
                break 
        if not found_better:
            return None

def steepest_ascent_hill_climbing(start_state, goal_state):
    current_state = fast_copy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    path = []
    while True:
        if current_state == goal_state:
            return path
        x, y = find_empty_tile(current_state)
        moves = p_moves(x, y)
        best_next_state = None
        best_action = None
        best_next_h = float('inf')
        for action in moves:
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            next_h = manhattan_distance(next_state, goal_state)
            if next_h < best_next_h:
                best_next_h = next_h
                best_next_state = next_state
                best_action = action
        if best_next_h >= current_h:
            return None
        current_state = best_next_state
        current_h = best_next_h
        path.append(best_action)

def stochastic_hill_climbing(start_state, goal_state):
    current_state = fast_copy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    path = []
    while True:
        if current_state == goal_state:
            return path
        x, y = find_empty_tile(current_state)
        moves = p_moves(x, y)
        better_neighbors = [] 
        for action in moves:
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            next_h = manhattan_distance(next_state, goal_state)
            if next_h < current_h:
                better_neighbors.append((next_state, action, next_h))
        if len(better_neighbors) == 0:
            return None
        else:
            chosen_neighbor = random.choice(better_neighbors)
            next_state, chosen_action, next_h = chosen_neighbor
            current_state = next_state
            current_h = next_h
            path.append(chosen_action)

def random_restart_hill_climbing(start_state, goal_state, max_restart=50):
    for i in range(max_restart):
        current_state = fast_copy(start_state)
        current_h = manhattan_distance(current_state, goal_state)
        path = []
        while True:
            if current_state == goal_state:
                return path, i + 1
            x, y = find_empty_tile(current_state)
            moves = p_moves(x, y)
            better_neighbors = [] 
            for action in moves:
                next_state = fast_copy(current_state)
                nx, ny = move(x, y, action)
                next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
                next_h = manhattan_distance(next_state, goal_state)
                if next_h < current_h:
                    better_neighbors.append((next_state, action, next_h))
            if len(better_neighbors) == 0:
                break 
            else:
                chosen_neighbor = random.choice(better_neighbors)
                next_state, chosen_action, next_h = chosen_neighbor
                current_state = next_state
                current_h = next_h
                path.append(chosen_action)
    return None, None

def random_state_from_start(start_state, steps=5):
    state = fast_copy(start_state)
    path = []
    for _ in range(steps):
        x, y = find_empty_tile(state)
        action = random.choice(p_moves(x, y))
        nx, ny = move(x, y, action)
        state[x][y], state[nx][ny] = state[nx][ny], state[x][y]
        path.append(action)
    return state, path

def local_beam_search(start_state, goal_state, k):
    if start_state == goal_state: return []
    current_state_set = []
    visited = set()
    for i in range(k):
        board, init_path = random_state_from_start(start_state, steps=5)
        board_str = state_to_str(board)
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
            if current_board == goal_state:
                return current_path 
            x, y = find_empty_tile(current_board)
            moves = p_moves(x, y)
            for action in moves:
                next_board = fast_copy(current_board)
                nx, ny = move(x, y, action)
                next_board[x][y], next_board[nx][ny] = next_board[nx][ny], next_board[x][y]
                board_str = state_to_str(next_board)
                if board_str not in visited:
                    visited.add(board_str)
                    neighbor_states.append({
                        'board': next_board,
                        'path': current_path + [action],
                        'h': manhattan_distance(next_board, goal_state)
                    })  
        for neighbor in neighbor_states:
            if neighbor['board'] == goal_state:
                return neighbor['path']
        if len(neighbor_states) == 0:
            return None
        neighbor_states.sort(key=lambda item: item['h'])
        current_state_set = neighbor_states[:k]

def simulated_annealing(start_state, goal_state, T0=10000, Tmin=0.001, alpha=0.9995):
    current_state = fast_copy(start_state)
    current_h = manhattan_distance(current_state, goal_state)
    T = T0
    path = []
    while T > Tmin:
        if current_state == goal_state:
            return path
        x, y = find_empty_tile(current_state)
        moves = p_moves(x, y)
        action = random.choice(moves)
        nx, ny = move(x, y, action)
        next_state = fast_copy(current_state)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        next_h = manhattan_distance(next_state, goal_state)
        delta = next_h - current_h
        if delta < 0:
            current_state = next_state
            current_h = next_h
            path.append(action)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_state = next_state
                current_h = next_h
                path.append(action)
        T = alpha * T
    return None 

def adversarial_utility(state, goal_state):
    if state == goal_state: return 1000 
    return -manhattan_distance(state, goal_state)

def adversarial_is_terminal(state, goal_state, depth):
    return state == goal_state or depth == 0

def minimax_step(state, goal_state, depth):
    value, best_move = minimax_max_value(state, goal_state, depth)
    return best_move

def minimax_max_value(state, goal_state, depth):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = -float('inf')
    best_move = None
    x, y = find_empty_tile(state)
    for action in p_moves(x, y):
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, _ = minimax_min_value(next_state, goal_state, depth - 1)
        if v2 > v:
            v = v2
            best_move = action
    return v, best_move

def minimax_min_value(state, goal_state, depth):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = float('inf')
    best_move = None
    x, y = find_empty_tile(state)
    for action in p_moves(x, y):
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, _ = minimax_max_value(next_state, goal_state, depth - 1)
        if v2 < v:
            v = v2
            best_move = action
    return v, best_move

def minimax_full_search(start_state, goal_state, depth_limit=4, max_steps=50):
    current_state = fast_copy(start_state)
    path = []
    previous_action = None
    step = 0
    while current_state != goal_state and step < max_steps:
        step += 1
        best_move = None
        max_v = -float('inf')
        x, y = find_empty_tile(current_state)
        for action in p_moves(x, y):
            if previous_action == 'U' and action == 'D': continue
            if previous_action == 'D' and action == 'U': continue
            if previous_action == 'L' and action == 'R': continue
            if previous_action == 'R' and action == 'L': continue
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            v, _ = minimax_min_value(next_state, goal_state, depth_limit - 1)
            if v > max_v:
                max_v = v
                best_move = action    
        if best_move is None:
            best_move = minimax_step(current_state, goal_state, depth_limit)
        if best_move is None: break
        path.append(best_move)
        nx, ny = move(x, y, best_move)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        previous_action = best_move
    if current_state == goal_state:
        return path
    return None

def alpha_beta_step(state, goal_state, depth):
    value, best_move = alpha_beta_max_value(state, goal_state, depth, -float('inf'), float('inf'))
    return best_move

def alpha_beta_max_value(state, goal_state, depth, alpha, beta):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = -float('inf')
    best_move = None
    x, y = find_empty_tile(state)
    for action in p_moves(x, y):
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, a2 = alpha_beta_min_value(next_state, goal_state, depth - 1, alpha, beta)
        if v2 > v:
            v = v2
            best_move = action
            alpha = max(alpha, v)
        if v >= beta:
            return v, best_move 
    return v, best_move

def alpha_beta_min_value(state, goal_state, depth, alpha, beta):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = float('inf')
    best_move = None
    x, y = find_empty_tile(state)
    for action in p_moves(x, y):
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, a2 = alpha_beta_max_value(next_state, goal_state, depth - 1, alpha, beta)
        if v2 < v:
            v = v2
            best_move = action
            beta = min(beta, v)
        if v <= alpha:
            return v, best_move     
    return v, best_move

def alpha_beta_full_search(start_state, goal_state, depth_limit=4, max_steps=50):
    current_state = fast_copy(start_state)
    path = []
    previous_action = None
    step = 0
    while current_state != goal_state and step < max_steps:
        step += 1
        best_move = None
        max_v = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        x, y = find_empty_tile(current_state)
        for action in p_moves(x, y):
            if previous_action == 'U' and action == 'D': continue
            if previous_action == 'D' and action == 'U': continue
            if previous_action == 'L' and action == 'R': continue
            if previous_action == 'R' and action == 'L': continue
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            v, _ = alpha_beta_min_value(next_state, goal_state, depth_limit - 1, alpha, beta)
            if v > max_v:
                max_v = v
                best_move = action    
            alpha = max(alpha, max_v)
        if best_move is None:
            best_move = alpha_beta_step(current_state, goal_state, depth_limit)
        if best_move is None: break
        path.append(best_move)
        nx, ny = move(x, y, best_move)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        previous_action = best_move
    if current_state == goal_state:
        return path
    return None

def expectimax_step(state, goal_state, depth):
    value, best_move = expectimax_max_value(state, goal_state, depth)
    return best_move

def expectimax_max_value(state, goal_state, depth):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = -float('inf')
    best_move = None
    x, y = find_empty_tile(state)
    for action in p_moves(x, y):
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, _ = expectimax_exp_value(next_state, goal_state, depth - 1)
        if v2 > v:
            v = v2
            best_move = action 
    return v, best_move

def expectimax_exp_value(state, goal_state, depth):
    if adversarial_is_terminal(state, goal_state, depth):
        return adversarial_utility(state, goal_state), None
    v = 0
    x, y = find_empty_tile(state)
    moves = p_moves(x, y)
    probability = 1.0 / len(moves)
    for action in moves:
        next_state = fast_copy(state)
        nx, ny = move(x, y, action)
        next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
        v2, _ = expectimax_max_value(next_state, goal_state, depth - 1)
        v += probability * v2
    return v, None

def expectimax_full_search(start_state, goal_state, depth_limit=4, max_steps=50):
    current_state = fast_copy(start_state)
    path = []
    previous_action = None
    step = 0
    while current_state != goal_state and step < max_steps:
        step += 1
        best_move = None
        max_v = -float('inf') 
        x, y = find_empty_tile(current_state)
        for action in p_moves(x, y):
            if previous_action == 'U' and action == 'D': continue
            if previous_action == 'D' and action == 'U': continue
            if previous_action == 'L' and action == 'R': continue
            if previous_action == 'R' and action == 'L': continue
            next_state = fast_copy(current_state)
            nx, ny = move(x, y, action)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            v, _ = expectimax_exp_value(next_state, goal_state, depth_limit - 1)
            if v > max_v:
                max_v = v
                best_move = action      
        if best_move is None:
            best_move = expectimax_step(current_state, goal_state, depth_limit)
        if best_move is None: break
        path.append(best_move)
        nx, ny = move(x, y, best_move)
        current_state[x][y], current_state[nx][ny] = current_state[nx][ny], current_state[x][y]
        previous_action = best_move
    if current_state == goal_state:
        return path
    return None

def apply_action(state, action):
    x, y = find_empty_tile(state)
    if action not in p_moves(x, y):
        return fast_copy(state) 
    nx, ny = move(x, y, action)
    new_state = fast_copy(state)
    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
    return new_state

def h_belief(belief, goal_state):
    return sum(manhattan_distance(s, goal_state) for s in belief)

def belief_to_tuple(belief):
    return tuple(state_to_tuple(s) for s in belief)

def sorted_belief_to_tuple(belief):
    unique_states = []
    for s in belief:
        if s not in unique_states:
            unique_states.append(s)
    return tuple(sorted(tuple(state_to_tuple(s)) for s in unique_states))

def belief_state_search(start_belief, goal_state):
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
        if all(s == goal_state for s in current_belief):
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
            x, y = find_empty_tile(s)
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
    return None, start_belief, "Thất bại"

def dfs_belief(start_belief, goal_state):
    frontier = [(start_belief, [])]
    explored = set()
    while frontier:
        node, path = frontier.pop()
        node_tuple = sorted_belief_to_tuple(node)
        if node_tuple in explored:
            continue
        explored.add(node_tuple)
        if all(s == goal_state for s in node):
            return path
        for action in ['U', 'R', 'L', 'D']:
            child_belief = [apply_action(s, action) for s in node]
            child_tuple = sorted_belief_to_tuple(child_belief)
            if child_tuple not in explored:
                frontier.append((child_belief, path + [action]))
    return None

def is_belief_goal_sensorless(belief, goal_states_list):
    for g in goal_states_list:
        if all(state_to_str(s) == state_to_str(g) for s in belief):
            return True
    return False

def sensorless_dfs(start_belief, goal_states_list):
    if is_belief_goal_sensorless(start_belief, goal_states_list):
        return []
    frontier = [(start_belief, [])]
    explored = set()
    while frontier:
        node, path = frontier.pop()
        node_tuple = sorted_belief_to_tuple(node)
        if node_tuple in explored:
            continue
        explored.add(node_tuple)
        if is_belief_goal_sensorless(node, goal_states_list):
            return path 
        all_act = set()
        for s in node:
            x, y = find_empty_tile(s)
            for a in p_moves(x, y):
                all_act.add(a)        
        for action in ['D', 'R', 'L', 'U']:
            if action not in all_act:
                continue
            child_belief = [apply_action(s, action) for s in node]
            child_tuple = sorted_belief_to_tuple(child_belief)
            if child_tuple not in explored:
                frontier.append((child_belief, path + [action]))     
    return None

def and_or_graph_search(start_state, goal_state, max_depth=30):
    FAILURE = "FAILURE"
    def or_search(state, path, depth_limit):
        if state == goal_state:
            return []
        state_tuple = state_to_tuple(state)
        if state_tuple in path:
            return FAILURE
        if depth_limit == 0:
            return FAILURE
        x, y = find_empty_tile(state)
        for action in p_moves(x, y):
            nx, ny = move(x, y, action)
            next_state = fast_copy(state)
            next_state[x][y], next_state[nx][ny] = next_state[nx][ny], next_state[x][y]
            result_states = [next_state]
            plan = and_search(result_states, path | {state_tuple}, depth_limit - 1)
            if plan is not FAILURE:
                return [action, plan]
        return FAILURE
    def and_search(states, path, depth_limit):
        plans = {}
        for s in states:
            plan_s = or_search(s, path, depth_limit)
            if plan_s is FAILURE:
                return FAILURE
            plans[state_to_tuple(s)] = plan_s
        return plans
    for depth in range(1, max_depth + 1):
        plan = or_search(start_state, set(), depth)
        if plan is not FAILURE:
            actions = []
            current = plan
            while current and isinstance(current, list):
                action, sub_plans = current[0], current[1]
                actions.append(action)
                if not sub_plans:
                    break
                current = next(iter(sub_plans.values()))
            return actions
    return None

VARS = list(range(9))

def neighbors_of(xi):
    return [xj for xj in VARS if xj != xi]

def remove_first(queue):
    return queue.popleft()

def satisfies(x, y):
    return x != y

def rm_inconsistent_values(domains, xi, xj):
    removed = False
    for x in list(domains[xi]):
        if not any(satisfies(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            removed = True
    return removed

def ac3(domains, neighbors):
    queue = deque()
    for xi in VARS:
        for xj in neighbors[xi]:
            queue.append((xi, xj))
    while queue:
        xi, xj = remove_first(queue)
        if rm_inconsistent_values(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def ac3_wrapper(start_state):
    flat = [val for row in start_state for val in row]
    domains = {i: {v} if v != -1 else set(range(9)) for i, v in enumerate(flat)}
    neighbors = {xi: neighbors_of(xi) for xi in VARS}
    def backtrack(curr_domains):
        if not ac3(curr_domains, neighbors):
            return None
        if all(len(d) == 1 for d in curr_domains.values()):
            board = [next(iter(curr_domains[i])) for i in VARS]
            new_state = [board[i*3:(i+1)*3] for i in range(3)]
            if is_solvable(new_state):
                return new_state
            return None
        unassigned = [i for i in VARS if len(curr_domains[i]) > 1]
        if not unassigned:
            return None
        var = unassigned[0]
        for value in curr_domains[var]:
            new_domains = {k: v.copy() for k, v in curr_domains.items()}
            new_domains[var] = {value}
            result = backtrack(new_domains)
            if result:
                return result
        return None
    solved_state = backtrack(domains)
    if solved_state:
        final_domains = {i: {solved_state[i//3][i%3]} for i in VARS}
        return ['AC3_SOLVED'], solved_state, final_domains
    else:
        return ['AC3_FAIL'], None, domains

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
    if current_state == goal_state:
        return list(path)
    x, y = find_empty_tile(current_state)
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
    working_state = fast_copy(start_state)
    visited = set()
    visited.add(state_to_tuple(working_state))
    return forward_check(working_state, goal_state, [], visited)

def min_conflicts_search(start_state, goal_state, max_steps=1000):
    current = fast_copy(start_state)
    path = []
    for step in range(max_steps):
        if current == goal_state:
            return path
        x, y = find_empty_tile(current)
        moves = p_moves(x, y)
        best_moves = []
        min_conflict_val = float('inf')
        for action in moves:
            nx, ny = move(x, y, action)
            neighbor = fast_copy(current)
            neighbor[x][y], neighbor[nx][ny] = neighbor[nx][ny], neighbor[x][y]
            conflict_val = manhattan_distance(neighbor, goal_state)
            if conflict_val < min_conflict_val:
                min_conflict_val = conflict_val
                best_moves = [(action, neighbor)]
            elif conflict_val == min_conflict_val:
                best_moves.append((action, neighbor))
        best_action, next_state = random.choice(best_moves)
        path.append(best_action)
        current = next_state   
    return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8_puzzle solver")
        self.root.geometry("950x750")
        self.root.configure(bg="#F5F5F7")
        self.font_main = ("Helvetica Neue", 12)
        
        self.current_state = fast_copy(START_STATE)
        self.initial_puzzle_state = fast_copy(START_STATE)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        self.algo_categories = {
            "Uninformed search algorithms": ["BFS", "DFS", "IDS", "UCS"],
            "Informed search algorithms": ["A*", "Greedy Search (GS)", "IDA*"],
            "Local search": ["Simple Hill Climbing", "Steepest Ascent Hill Climbing", "Stochastic Hill Climbing", "Local Beam Search", "Random Restart Hill Climbing", "Simulated Annealing"],
            "Searching in complex environments": ["AND-OR Graph Search", "Belief State Search (A*)", "Belief State Search (DFS)", "Sensorless Search (DFS)"],
            "Constraint satisfaction problems": ["AC-3", "Backtracking Search", "Forward Checking", "Min-Conflicts"],
            "Tìm kiếm đối kháng": ["Minimax Search", "Alpha-Beta Pruning", "Expectimax Search"]
        }
        
        self.is_solving = False
        self.is_paused = False
        self.auto_play_mode = True 
        self.path = []
        self.path_index = 0
        self.extra_info = None 
        
        self.create_widgets()
        self.update_board()

    def draw_mini_board(self, parent, title, state):
        frame = tk.Frame(parent, bg="#F5F5F7")
        tk.Label(frame, text=title, font=("Helvetica Neue", 10, "bold"), bg="#F5F5F7", fg="#555555").pack(pady=(0, 2))
        
        grid_border = tk.Frame(frame, bg="#DDDDDD", bd=1)
        grid_border.pack()
        inner = tk.Frame(grid_border, bg="#E0E0E2", padx=2, pady=2)
        inner.pack()
        
        labels = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                text = str(val) if val > 0 else ("?" if val == -1 else "")
                bg_color = "#FFFFFF" if val > 0 else ("#FFD54F" if val == -1 else "#E0E0E2")
                lbl = tk.Label(inner, text=text, width=2, height=1, font=("Helvetica Neue", 10, "bold"), bg=bg_color, fg="#333333")
                lbl.grid(row=i, column=j, padx=1, pady=1)
                labels[i][j] = lbl
        return frame, labels

    def update_mini_board(self, labels, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                text = str(val) if val > 0 else ("?" if val == -1 else "")
                bg_color = "#FFFFFF" if val > 0 else ("#FFD54F" if val == -1 else "#E0E0E2")
                labels[i][j].config(text=text, bg=bg_color)

    def create_widgets(self):
        left_frame = tk.Frame(self.root, bg="#F5F5F7", width=420)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        
        top_boards_frame = tk.Frame(left_frame, bg="#F5F5F7")
        top_boards_frame.pack(pady=(0, 15))

        start_frame, self.start_labels = self.draw_mini_board(top_boards_frame, "START", self.current_state)
        start_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(top_boards_frame, text="➔", font=("Helvetica Neue", 20), bg="#F5F5F7", fg="#AAAAAA").pack(side=tk.LEFT, padx=15)

        goal_frame, _ = self.draw_mini_board(top_boards_frame, "GOAL", GOAL_STATE)
        goal_frame.pack(side=tk.LEFT, padx=10)

        grid_frame = tk.Frame(left_frame, bg="#DDDDDD", bd=2)
        grid_frame.pack(pady=10)
        inner_grid = tk.Frame(grid_frame, bg="#E0E0E2", padx=5, pady=5)
        inner_grid.pack()
        
        for i in range(3):
            for j in range(3):
                btn = tk.Button(inner_grid, text="", font=("Helvetica Neue", 28, "bold"), width=4, height=1, relief="flat", bg="#FFFFFF")
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.buttons[i][j] = btn

        btn_frame = tk.Frame(left_frame, bg="#F5F5F7")
        btn_frame.pack(pady=15)
        
        self.btn_new = tk.Button(btn_frame, text="Tạo Mới", font=self.font_main, bg="#FF9800", fg="white", width=9, relief="flat", command=self.generate_new_puzzle)
        self.btn_new.grid(row=0, column=0, padx=4, pady=5)
        
        self.btn_new_csp = tk.Button(btn_frame, text="Tạo Khuyết", font=self.font_main, bg="#AB47BC", fg="white", width=9, relief="flat", command=self.generate_csp_puzzle)
        
        self.btn_solve = tk.Button(btn_frame, text="Chạy", font=self.font_main, bg="#4CAF50", fg="white", width=9, relief="flat", command=lambda: self.start_solving(auto_play=True))
        self.btn_solve.grid(row=0, column=1, padx=4, pady=5)
        
        self.btn_reset = tk.Button(btn_frame, text="Reset", font=self.font_main, bg="#607D8B", fg="white", width=9, relief="flat", command=self.reset_board)
        self.btn_reset.grid(row=0, column=2, padx=4, pady=5)
        
        self.btn_pause = tk.Button(btn_frame, text="Dừng", font=self.font_main, bg="#8E8E93", fg="white", width=18, relief="flat", command=self.toggle_pause, state=tk.DISABLED)
        self.btn_pause.grid(row=1, column=0, columnspan=2, sticky="we", padx=4, pady=5)
        
        self.btn_step = tk.Button(btn_frame, text="Bước tiếp", font=self.font_main, bg="#4FC3F7", fg="white", width=9, relief="flat", command=self.next_step, state=tk.NORMAL)
        self.btn_step.grid(row=1, column=2, columnspan=1, sticky="we", padx=4, pady=5)

        tk.Label(left_frame, text="Nhóm thuật toán:", font=self.font_main, bg="#F5F5F7").pack(pady=(10, 0))
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(left_frame, textvariable=self.cat_var, font=self.font_main, state="readonly", width=30)
        self.cat_combo['values'] = list(self.algo_categories.keys())
        self.cat_combo.current(0)
        self.cat_combo.pack(pady=5)
        self.cat_combo.bind("<<ComboboxSelected>>", self.update_algo_list)
        
        tk.Label(left_frame, text="Chọn thuật toán:", font=self.font_main, bg="#F5F5F7").pack(pady=(5, 0))
        
        self.algo_row_frame = tk.Frame(left_frame, bg="#F5F5F7")
        self.algo_row_frame.pack(pady=5)

        self.algo_var = tk.StringVar()
        self.algo_combo = ttk.Combobox(self.algo_row_frame, textvariable=self.algo_var, font=self.font_main, state="readonly", width=24)
        self.algo_combo.pack(side=tk.LEFT)
        self.algo_combo.bind("<<ComboboxSelected>>", self.on_algo_changed)

        self.k_frame = tk.Frame(self.algo_row_frame, bg="#F5F5F7")
        tk.Label(self.k_frame, text="k:", font=self.font_main, bg="#F5F5F7", fg="#333333").pack(side=tk.LEFT, padx=(10, 2))
        self.k_var = tk.IntVar(value=4)
        self.k_spin = tk.Spinbox(self.k_frame, from_=1, to=20, textvariable=self.k_var, width=3, font=self.font_main)
        self.k_spin.pack(side=tk.LEFT)

        self.restart_frame = tk.Frame(self.algo_row_frame, bg="#F5F5F7")
        tk.Label(self.restart_frame, text="Restarts:", font=self.font_main, bg="#F5F5F7", fg="#333333").pack(side=tk.LEFT, padx=(10, 2))
        self.restart_var = tk.IntVar(value=30)
        self.restart_spin = tk.Spinbox(self.restart_frame, from_=1, to=100, textvariable=self.restart_var, width=4, font=self.font_main)
        self.restart_spin.pack(side=tk.LEFT)

        self.update_algo_list(None)

        self.status_label = tk.Label(left_frame, text="Sẵn sàng!", font=("Helvetica Neue", 12, "italic"), bg="#F5F5F7", fg="#555555")
        self.status_label.pack(pady=10)

        ttk.Separator(self.root, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=20)

        right_frame = tk.Frame(self.root, bg="#F5F5F7")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(right_frame, text="Các bước chạy chi tiết:", font=("Helvetica Neue", 14, "bold"), bg="#F5F5F7").pack(anchor="w")
        
        self.text_log = scrolledtext.ScrolledText(right_frame, font=("Courier", 11), width=45, height=20, state='disabled')
        self.text_log.pack(pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(right_frame, text="Chuỗi hành động đi:", font=("Helvetica Neue", 12, "bold"), bg="#F5F5F7").pack(anchor="w", pady=(10, 5))
        
        self.action_log = tk.Text(right_frame, font=("Helvetica Neue", 11), height=3, wrap=tk.WORD, state='disabled', bg="#EFEFF4")
        self.action_log.pack(fill=tk.X)

    def update_algo_list(self, event):
        selected_cat = self.cat_var.get()
        algos = self.algo_categories[selected_cat]
        self.algo_combo['values'] = algos
        self.algo_combo.current(0)
        self.on_algo_changed()

    def on_algo_changed(self, event=None):
        algo = self.algo_var.get()
        self.k_frame.pack_forget()
        self.restart_frame.pack_forget()
        
        if algo == "Local Beam Search":
            self.k_frame.pack(side=tk.LEFT)
            self.k_spin.config(state=tk.NORMAL)
        elif algo == "Random Restart Hill Climbing":
            self.restart_frame.pack(side=tk.LEFT)
            self.restart_spin.config(state=tk.NORMAL)

        if algo == "AC-3":
            self.btn_new_csp.grid(row=0, column=3, padx=4, pady=5)
        else:
            self.btn_new_csp.grid_remove()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                val = self.current_state[i][j]
                if val == 0:
                    self.buttons[i][j].config(text="", bg="#E0E0E2")
                elif val == -1:
                    self.buttons[i][j].config(text="?", bg="#FFD54F", fg="#D84315")
                else:
                    self.buttons[i][j].config(text=str(val), bg="#FFFFFF", fg="#333333")
                    
    def format_board_str(self, board):
        res = ""
        for row in board:
            res += " ".join(f"{str(x):>2}" if x > 0 else (" ?" if x == -1 else " _") for x in row) + "\n"
        return res

    def log_message(self, message, is_action=False):
        widget = self.action_log if is_action else self.text_log
        widget.config(state='normal')
        widget.insert(tk.END, message + "\n")
        widget.see(tk.END)
        widget.config(state='disabled')
        
    def clear_logs(self):
        for widget in (self.text_log, self.action_log):
            widget.config(state='normal')
            widget.delete(1.0, tk.END)
            widget.config(state='disabled')

    def generate_new_puzzle(self):
        self.current_state = fast_copy(GOAL_STATE)
        steps = random.randint(20, 30)
        for _ in range(steps):
            x, y = find_empty_tile(self.current_state)
            moves = p_moves(x, y)
            action = random.choice(moves)
            nx, ny = move(x, y, action)
            self.current_state[x][y], self.current_state[nx][ny] = self.current_state[nx][ny], self.current_state[x][y]
        
        self.initial_puzzle_state = fast_copy(self.current_state)
        self.is_solving = False
        self.is_paused = False
        
        self.update_board()
        self.update_mini_board(self.start_labels, self.current_state)
        self.clear_logs()
        
        self.btn_step.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED, text="Dừng", bg="#8E8E93")
        
        inv_count = count_inversions(self.current_state)
        self.status_label.config(text=f"Đã tạo trạng thái! (Nghịch thế: {inv_count})", fg="#FF9500")

    def generate_csp_puzzle(self):
        self.current_state = fast_copy(GOAL_STATE)
        steps = random.randint(20, 30)
        for _ in range(steps):
            x, y = find_empty_tile(self.current_state)
            moves = p_moves(x, y)
            action = random.choice(moves)
            nx, ny = move(x, y, action)
            self.current_state[x][y], self.current_state[nx][ny] = self.current_state[nx][ny], self.current_state[x][y]
        
        tiles = [(r, c) for r in range(3) for c in range(3)]
        to_remove = random.sample(tiles, 2) 
        for r, c in to_remove:
            self.current_state[r][c] = -1
            
        self.initial_puzzle_state = fast_copy(self.current_state)
        self.is_solving = False
        self.is_paused = False
        
        self.update_board()
        self.update_mini_board(self.start_labels, self.current_state)
        self.clear_logs()
        
        self.btn_step.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED, text="Dừng", bg="#8E8E93")
        
        self.status_label.config(text="Đã tạo bảng CSP (có ô khuyết)!", fg="#AB47BC")
        
        csp_index = list(self.algo_categories.keys()).index("Constraint satisfaction problems")
        self.cat_combo.current(csp_index)
        self.update_algo_list(None)

    def reset_board(self):
        self.is_solving = False
        self.is_paused = False
        self.path = []
        self.path_index = 0
        
        self.current_state = fast_copy(self.initial_puzzle_state)
        self.update_board()
        self.clear_logs()
        
        self.btn_new.config(state=tk.NORMAL)
        self.btn_new_csp.config(state=tk.NORMAL)
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_step.config(state=tk.NORMAL) 
        self.algo_combo.config(state="readonly")
        self.cat_combo.config(state="readonly")
        self.on_algo_changed() 
        
        self.btn_pause.config(state=tk.DISABLED, text="Dừng", bg="#8E8E93")
        self.status_label.config(text="Đã reset về trạng thái ban đầu.", fg="#555555")

    def toggle_pause(self):
        if not self.is_solving: return
        
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.config(text="Tiếp tục", bg="#FF9500") 
            self.btn_step.config(state=tk.NORMAL)
            self.status_label.config(text="Đã tạm dừng", fg="#FF9500")
        else:
            self.btn_pause.config(text="Dừng", bg="#E53935") 
            self.btn_step.config(state=tk.DISABLED)
            self.status_label.config(text="Đang chạy...", fg="#007AFF")
            self.animate_step()

    def next_step(self):
        if not self.is_solving:
            self.start_solving(auto_play=False)
        elif self.is_paused:
            if self.path_index < len(self.path):
                self._execute_single_step()
                if self.path_index >= len(self.path):
                    self._finish_solving()

    def start_solving(self, auto_play=True):
        algo_name = self.algo_var.get()
        
        if algo_name != "AC-3" and any(-1 in row for row in self.current_state):
            messagebox.showerror("Lỗi", "Bảng đang có ô khuyết (Bài toán CSP).\nVui lòng chọn thuật toán 'AC-3' để điền số trước khi tìm đường đi!")
            return

        if algo_name == "AC-3" and not any(-1 in row for row in self.current_state):
            messagebox.showinfo("Thông báo", "Bảng hiện tại đã đầy đủ!\nVui lòng bấm 'Tạo Khuyết' trước khi chạy AC-3.")
            return

        if self.current_state == GOAL_STATE:
            messagebox.showinfo("Thông báo", "Bảng đã ở trạng thái đích (GOAL)!")
            return

        if algo_name != "AC-3":
            inv_count = count_inversions(self.current_state)
            if not is_solvable(self.current_state):
                err_msg = f"KHÔNG THỂ GIẢI!\n\nSố cặp nghịch thế là {inv_count} (số lẻ).\nChỉ bảng có nghịch thế CHẴN mới có thể chuyển về GOAL."
                messagebox.showerror("Lỗi Thuật Toán", err_msg)
                self.status_label.config(text=f"Lỗi: Nghịch thế lẻ ({inv_count})", fg="#FF3B30")
                return

        self.auto_play_mode = auto_play
        k_val = self.k_var.get() 
        restart_val = self.restart_var.get()
        
        self.status_label.config(text=f"Đang chạy {algo_name}...", fg="#007AFF")
        
        self.btn_new.config(state=tk.DISABLED)
        self.btn_new_csp.config(state=tk.DISABLED)
        self.btn_solve.config(state=tk.DISABLED)
        self.btn_reset.config(state=tk.DISABLED)
        self.btn_step.config(state=tk.DISABLED) 
        self.algo_combo.config(state=tk.DISABLED)
        self.cat_combo.config(state=tk.DISABLED)
        self.k_spin.config(state=tk.DISABLED) 
        self.restart_spin.config(state=tk.DISABLED)
        
        self.clear_logs()
        
        if algo_name == "AC-3":
            self.log_message("--- CHẠY THUẬT TOÁN AC-3 ---")
        else:
            self.log_message(f"--- BẮT ĐẦU TÌM KIẾM ({algo_name}) ---")
            
        self.log_message(f"Trạng thái ban đầu:\n{self.format_board_str(self.current_state)}")
        
        thread = threading.Thread(target=self.run_algorithm_in_background, args=(algo_name, k_val, restart_val))
        thread.daemon = True
        thread.start()

    def run_algorithm_in_background(self, algo_name, k_val, restart_val):
        path = None
        extra_info = None
        
        if algo_name == "BFS": path = bfs(self.current_state, GOAL_STATE)
        elif algo_name == "DFS": path = dfs(self.current_state, GOAL_STATE)
        elif algo_name == "Backtracking Search": path = backtracking_search(self.current_state, GOAL_STATE)
        elif algo_name == "Forward Checking": path = forward_checking_search(self.current_state, GOAL_STATE)
        elif algo_name == "Min-Conflicts": path = min_conflicts_search(self.current_state, GOAL_STATE)
        elif algo_name == "IDS": path = ids(self.current_state, GOAL_STATE)
        elif algo_name == "UCS": path = ucs(self.current_state, GOAL_STATE)
        elif algo_name == "A*": path = a_star_search(self.current_state, GOAL_STATE)
        elif algo_name == "Greedy Search (GS)": path = greedy_search(self.current_state, GOAL_STATE)
        elif algo_name == "IDA*": path = ida_star_search(self.current_state, GOAL_STATE)
        elif algo_name == "Simple Hill Climbing": path = simple_hill_climbing(self.current_state, GOAL_STATE) 
        elif algo_name == "Steepest Ascent Hill Climbing": path = steepest_ascent_hill_climbing(self.current_state, GOAL_STATE)
        elif algo_name == "Stochastic Hill Climbing": path = stochastic_hill_climbing(self.current_state, GOAL_STATE)
        elif algo_name == "Local Beam Search": path = local_beam_search(self.current_state, GOAL_STATE, k=k_val)
        elif algo_name == "Random Restart Hill Climbing": 
            path, extra_info = random_restart_hill_climbing(self.current_state, GOAL_STATE, max_restart=restart_val)
        elif algo_name == "Simulated Annealing": path = simulated_annealing(self.current_state, GOAL_STATE)
        elif algo_name == "AND-OR Graph Search": path = and_or_graph_search(self.current_state, GOAL_STATE, max_depth=30)
        elif algo_name == "Minimax Search": path = minimax_full_search(self.current_state, GOAL_STATE)
        elif algo_name == "Alpha-Beta Pruning": path = alpha_beta_full_search(self.current_state, GOAL_STATE)
        elif algo_name == "Expectimax Search": path = expectimax_full_search(self.current_state, GOAL_STATE)
        elif algo_name == "AC-3":
            path, new_state, domains = ac3_wrapper(self.current_state)
            extra_info = {'state': new_state, 'domains': domains}
        elif algo_name in ["Belief State Search (A*)", "Belief State Search (DFS)", "Sensorless Search (DFS)"]:
            x, y = find_empty_tile(self.current_state)
            moves = p_moves(x, y)
            alt_state = fast_copy(self.current_state)
            if moves:
                a = random.choice(moves)
                nx, ny = move(x, y, a)
                alt_state[x][y], alt_state[nx][ny] = alt_state[nx][ny], alt_state[x][y]
                
            start_belief = [self.current_state, alt_state]
            if algo_name == "Belief State Search (A*)":
                path, _, _ = belief_state_search(start_belief, GOAL_STATE)
            elif algo_name == "Belief State Search (DFS)":
                path = dfs_belief(start_belief, GOAL_STATE)
            elif algo_name == "Sensorless Search (DFS)":
                path = sensorless_dfs(start_belief, [GOAL_STATE])

        self.root.after(0, lambda: self.process_result(path, algo_name, extra_info))

    def process_result(self, path, algo_name, extra_info):
        if algo_name == "AC-3":
            if path and path[0] == 'AC3_SOLVED':
                self.current_state = extra_info['state']
                self.update_board()
                self.log_message("=> CSP NHẤT QUÁN! Đã giải mã toàn bộ ô khuyết thành cấu hình hợp lệ.")
                self.log_message(self.format_board_str(self.current_state))
                
                self.log_message("\n=> BƯỚC TIẾP THEO: Hãy đổi sang nhóm thuật toán Tìm Kiếm (VD: A*, BFS) và bấm 'Chạy' để giải 8-Puzzle!")
                self.status_label.config(text="Đã điền xong! Hãy chọn thuật toán giải đường đi.", fg="#4CAF50")
                
            elif path and path[0] == 'AC3_PARTIAL':
                self.log_message("=> CSP Nhất quán, nhưng CHƯA THỂ GIẢI ĐƯỢC HẾT!")
                self.log_message("Miền giá trị còn lại:")
                for i in range(9):
                    self.log_message(f"  Biến X{i}: {sorted(extra_info['domains'][i])}")
                self.status_label.config(text="AC-3: Chưa giải được hết", fg="#FF9500")
            else:
                self.log_message("=> CSP KHÔNG NHẤT QUÁN! Các miền giá trị xung đột.")
                self.status_label.config(text="AC-3: Không nhất quán", fg="#E53935")
            
            self.is_solving = False
            self.btn_new.config(state=tk.NORMAL)
            self.btn_new_csp.config(state=tk.NORMAL)
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_reset.config(state=tk.NORMAL)
            self.algo_combo.config(state="readonly")
            self.cat_combo.config(state="readonly")
            self.on_algo_changed()
            self.btn_pause.config(state=tk.DISABLED, text="Dừng", bg="#8E8E93")
            self.btn_step.config(state=tk.DISABLED)
            return

        if path is not None:
            self.path = path
            self.path_index = 0
            self.extra_info = extra_info 
            self.is_solving = True
            
            self.btn_reset.config(state=tk.NORMAL)
            
            if self.auto_play_mode:
                self.is_paused = False
                self.status_label.config(text=f"Đang chạy...", fg="#007AFF")
                self.btn_pause.config(state=tk.NORMAL, text="Dừng", bg="#E53935") 
                self.btn_step.config(state=tk.DISABLED)
                self.animate_step()
            else:
                self.is_paused = True
                self.status_label.config(text=f"Đã tạm dừng", fg="#FF9500")
                self.btn_pause.config(state=tk.NORMAL, text="Tiếp tục", bg="#FF9500")
                self.btn_step.config(state=tk.NORMAL)
                self._execute_single_step() 
        else:
            if algo_name in ["Simple Hill Climbing", "Steepest Ascent Hill Climbing", "Stochastic Hill Climbing", "Local Beam Search", "Random Restart Hill Climbing", "Simulated Annealing", "Min-Conflicts"]:
                err_text = "Không tìm thấy đường đi! (Local Optimum hoặc vượt quá số bước)"
            elif algo_name in ["Minimax Search", "Alpha-Beta Pruning", "Expectimax Search"]:
                err_text = "Không tìm thấy đường đi! (Kẹt hoặc vượt quá 50 bước)"
            elif algo_name in ["Belief State Search (A*)", "Belief State Search (DFS)", "AND-OR Graph Search", "Sensorless Search (DFS)"]:
                err_text = "Không tìm thấy chuỗi hành động chung / Không tìm thấy đường đi!"
            else:
                err_text = "Không tìm thấy đường đi!"
                
            self.status_label.config(text=err_text, fg="#FF3B30")
            self.btn_new.config(state=tk.NORMAL)
            self.btn_new_csp.config(state=tk.NORMAL)
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_reset.config(state=tk.NORMAL)
            self.btn_step.config(state=tk.NORMAL)
            self.algo_combo.config(state="readonly")
            self.cat_combo.config(state="readonly")
            self.on_algo_changed() 

    def get_delay(self):
        if len(self.path) > 1000: return 5
        elif len(self.path) > 300: return 20
        return 300

    def _execute_single_step(self):
        action = self.path[self.path_index]
        algo = self.algo_var.get()
        
        if algo in ["Belief State Search (A*)", "Belief State Search (DFS)", "Sensorless Search (DFS)"]:
            self.current_state = apply_action(self.current_state, action)
        else:
            x, y = find_empty_tile(self.current_state)
            nx, ny = move(x, y, action)
            self.current_state[x][y], self.current_state[nx][ny] = self.current_state[nx][ny], self.current_state[x][y]
            
        self.update_board()
        
        current_step = self.path_index + 1
        new_h = manhattan_distance(self.current_state, GOAL_STATE)
        new_f = current_step + new_h
        
        step_msg = f"Bước {current_step}: Di chuyển '{action}'"
        
        if algo == "IDS":
            step_msg += f"   (Depth: {current_step} / {len(self.path)})"
        elif algo == "UCS":
            step_msg += f"   (Cost g={current_step})"
        elif algo == "A*":
            step_msg += f"   (g={current_step}, h={new_h}, f={new_f})"
        elif algo == "IDA*":
            step_msg += f"   (Cost g={current_step}, h={new_h}, Threshold f={new_f})"
        elif algo == "Greedy Search (GS)":
            step_msg += f"   (Heuristic h={new_h})"
        elif algo == "Random Restart Hill Climbing":
            restart_num = self.extra_info if self.extra_info else 1
            step_msg += f"   (Restart: {restart_num} | h={new_h})"
        elif algo in ["Simple Hill Climbing", "Steepest Ascent Hill Climbing", "Stochastic Hill Climbing", "Local Beam Search", "Simulated Annealing", "Minimax Search", "Alpha-Beta Pruning", "Expectimax Search", "Min-Conflicts"]:
            step_msg += f"   (Heuristic h={new_h})"
            
        self.log_message(step_msg)
        self.log_message(self.format_board_str(self.current_state))
        
        self.path_index += 1

    def animate_step(self):
        if not self.is_solving: return
        if self.is_paused: return
        
        if self.path_index < len(self.path):
            self._execute_single_step()
            self.root.after(self.get_delay(), self.animate_step)
        else:
            self._finish_solving()

    def _finish_solving(self):
        self.is_solving = False
        self.log_message("-" * 65)
        self.log_message("ĐÃ ĐẠT TRẠNG THÁI ĐÍCH!")
        
        action_str = " -> ".join(self.path)
        self.log_message(action_str, is_action=True)
        self.status_label.config(text=f"Hoàn thành! Số bước: {len(self.path)}", fg="#4CAF50")
        
        self.btn_new.config(state=tk.NORMAL)
        self.btn_new_csp.config(state=tk.NORMAL)
        self.btn_solve.config(state=tk.NORMAL)
        self.algo_combo.config(state="readonly")
        self.cat_combo.config(state="readonly")
        self.on_algo_changed() 
        
        self.btn_pause.config(state=tk.DISABLED, text="Dừng", bg="#8E8E93")
        self.btn_step.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root) 
    root.mainloop()