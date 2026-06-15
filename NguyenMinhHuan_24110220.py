import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import threading
from collections import deque
import heapq

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
            if val != 0:
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

def bfs(start_state, goal_state):
    if start_state == goal_state: return []
    frontier = deque([(start_state, [])])
    explored = set([state_to_str(start_state)])

    while frontier:
        node, path = frontier.popleft()
        if node == goal_state:
            return path
        
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

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver Tổng Hợp")
        self.root.geometry("900x630")
        self.root.configure(bg="#F5F5F7")
        self.font_main = ("Helvetica Neue", 12)
        
        self.current_state = fast_copy(START_STATE)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
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
                text = str(val) if val != 0 else ""
                bg_color = "#FFFFFF" if val != 0 else "#E0E0E2"
                lbl = tk.Label(inner, text=text, width=2, height=1, font=("Helvetica Neue", 10, "bold"), bg=bg_color, fg="#333333")
                lbl.grid(row=i, column=j, padx=1, pady=1)
                labels[i][j] = lbl
        return frame, labels

    def update_mini_board(self, labels, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                text = str(val) if val != 0 else ""
                bg_color = "#FFFFFF" if val != 0 else "#E0E0E2"
                labels[i][j].config(text=text, bg=bg_color)

    def create_widgets(self):
        left_frame = tk.Frame(self.root, bg="#F5F5F7", width=400)
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
        
        self.btn_new = tk.Button(btn_frame, text="Tạo Mới", font=self.font_main, bg="#FF9500", fg="white", width=10, relief="flat", command=self.generate_new_puzzle)
        self.btn_new.grid(row=0, column=0, padx=10)
        
        self.btn_solve = tk.Button(btn_frame, text="Chạy", font=self.font_main, bg="#4CAF50", fg="white", width=10, relief="flat", command=self.start_solving)
        self.btn_solve.grid(row=0, column=1, padx=10)
        
        tk.Label(left_frame, text="Chọn thuật toán:", font=self.font_main, bg="#F5F5F7").pack(pady=(10, 0))
        self.algo_var = tk.StringVar(value="DFS") 
        self.algo_combo = ttk.Combobox(left_frame, textvariable=self.algo_var, font=self.font_main, state="readonly", width=15)
        self.algo_combo['values'] = ("BFS", "DFS", "IDS", "UCS")
        self.algo_combo.pack(pady=5)
        
        self.status_label = tk.Label(left_frame, text="Sẵn sàng!", font=("Helvetica Neue", 12, "italic"), bg="#F5F5F7", fg="#555555")
        self.status_label.pack(pady=15)

        ttk.Separator(self.root, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=20)

        right_frame = tk.Frame(self.root, bg="#F5F5F7")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(right_frame, text="Các bước chạy chi tiết:", font=("Helvetica Neue", 14, "bold"), bg="#F5F5F7").pack(anchor="w")
        
        self.text_log = scrolledtext.ScrolledText(right_frame, font=("Courier", 11), width=40, height=18, state='disabled')
        self.text_log.pack(pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(right_frame, text="Chuỗi hành động đi:", font=("Helvetica Neue", 12, "bold"), bg="#F5F5F7").pack(anchor="w", pady=(10, 5))
        
        self.action_log = tk.Text(right_frame, font=("Helvetica Neue", 11), height=3, wrap=tk.WORD, state='disabled', bg="#EFEFF4")
        self.action_log.pack(fill=tk.X)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                val = self.current_state[i][j]
                if val == 0:
                    self.buttons[i][j].config(text="", bg="#E0E0E2")
                else:
                    self.buttons[i][j].config(text=str(val), bg="#FFFFFF", fg="#333333")
                    
    def format_board_str(self, board):
        res = ""
        for row in board:
            res += " ".join(f"{str(x):>2}" if x != 0 else " _" for x in row) + "\n"
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
        
        self.update_board()
        self.update_mini_board(self.start_labels, self.current_state)
        self.clear_logs()
        
        inv_count = count_inversions(self.current_state)
        self.status_label.config(text=f"Đã tạo trạng thái! (Nghịch thế: {inv_count})", fg="#FF9500")

    def start_solving(self):
        if self.current_state == GOAL_STATE:
            messagebox.showinfo("Thông báo", "Bảng đã ở trạng thái đích (GOAL)!")
            return

        inv_count = count_inversions(self.current_state)
        if not is_solvable(self.current_state):
            err_msg = f"KHÔNG THỂ GIẢI!\n\nSố cặp nghịch thế là {inv_count} (số lẻ).\nTheo toán học, chỉ bảng có nghịch thế CHẴN mới có thể chuyển về GOAL được."
            messagebox.showerror("Lỗi Thuật Toán", err_msg)
            self.status_label.config(text=f"Lỗi: Nghịch thế lẻ ({inv_count})", fg="#FF3B30")
            return

        algo_name = self.algo_var.get()
        self.status_label.config(text=f"Đang giải bằng {algo_name}... Vui lòng đợi", fg="#007AFF")
        self.btn_new.config(state=tk.DISABLED)
        self.btn_solve.config(state=tk.DISABLED)
        self.algo_combo.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_algorithm_in_background, args=(algo_name,))
        thread.daemon = True
        thread.start()

    def run_algorithm_in_background(self, algo_name):
        path = None
        if algo_name == "BFS":
            path = bfs(self.current_state, GOAL_STATE)
        elif algo_name == "DFS":
            path = dfs(self.current_state, GOAL_STATE)
        elif algo_name == "IDS":
            path = ids(self.current_state, GOAL_STATE)
        elif algo_name == "UCS":
            path = ucs(self.current_state, GOAL_STATE)

        self.root.after(0, lambda: self.process_result(path, algo_name))

    def process_result(self, path, algo_name):
        if path is not None:
            self.clear_logs()
            self.log_message(f"--- BẮT ĐẦU GIẢI ({algo_name}) ---")
            self.log_message(f"Trạng thái ban đầu:\n{self.format_board_str(self.current_state)}")
            
            self.status_label.config(text=f"Đang chạy...", fg="#007AFF")
            
            self.animate_solution(path)
        else:
            self.status_label.config(text="Không tìm thấy đường đi!", fg="#FF3B30")
            self.btn_new.config(state=tk.NORMAL)
            self.btn_solve.config(state=tk.NORMAL)
            self.algo_combo.config(state="readonly")

    def animate_solution(self, path):
        simulated_state = fast_copy(self.current_state)
        
        delay = 300
        if len(path) > 1000:
            delay = 5
        elif len(path) > 300:
            delay = 20

        def step(index):
            if index < len(path):
                action = path[index]
                x, y = find_empty_tile(simulated_state)
                nx, ny = move(x, y, action)
                simulated_state[x][y], simulated_state[nx][ny] = simulated_state[nx][ny], simulated_state[x][y]
                
                self.current_state = fast_copy(simulated_state)
                self.update_board()
                
                self.log_message(f"Bước {index + 1}: Di chuyển '{action}'")
                self.log_message(self.format_board_str(self.current_state))
                
                self.root.after(delay, step, index + 1)
            else:
                self.log_message("ĐÃ ĐẠT TRẠNG THÁI ĐÍCH!")
                
                action_str = " -> ".join(path)
                self.log_message(action_str, is_action=True)
                self.status_label.config(text=f"Hoàn thành! Số bước: {len(path)}", fg="#4CAF50")
                
                self.btn_new.config(state=tk.NORMAL)
                self.btn_solve.config(state=tk.NORMAL)
                self.algo_combo.config(state="readonly")
                
        step(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()