import copy
import heapq
import tkinter as tk
from tkinter import messagebox

start = [[1, 2, 3],
         [4, 0, 6],
         [7, 5, 8]]

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

def tinh_cost(state, goal_state):
    cost = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                cost += 1
    return cost

def ucs(start_state, goal_state):
    if start_state == goal_state:
        return [], 0
    counter = 0
    frontier = []
    heapq.heappush(frontier, (0, counter, start_state, []))
    explored = []
    while frontier:
        current_cost, _, node, path = heapq.heappop(frontier)
        if node == goal_state:
            return path, current_cost
        if node in explored:
            continue
        explored.append(node)
        x, y = tim_o_trong(node)
        moves = p_moves(x, y)
        for action in moves:
            child = copy.deepcopy(node)
            nx, ny = move(x, y, action)
            child[x][y], child[nx][ny] = child[nx][ny], child[x][y]
            if child not in explored:
                weight = tinh_cost(child, goal_state)
                new_cost = current_cost + weight
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, child, path + [action]))   
    return None, None

def states_equal(a, b):
    for i in range(3):
        for j in range(3):
            if a[i][j] != b[i][j]:
                return False
    return True


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (UCS)")

        self.bg_color         = "#F5F5F7"
        self.tile_color       = "#FFFFFF"
        self.tile_text_color  = "#333333"
        self.blank_tile_color = "#E0E0E2"
        self.primary_color    = "#007AFF"
        self.success_color    = "#4CAF50"
        self.error_color      = "#FF3B30"
        self.text_color_main  = "#1C1C1E"
        self.text_color_sub   = "#8E8E93"

        self.font_family = "Helvetica Neue"
        self.root.option_add("*Font", (self.font_family, 12))
        self.root.configure(bg=self.bg_color)

        window_width = 450
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.minsize(window_width, window_height)

        self.current_state = copy.deepcopy(start)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=(30, 20))

        tk.Label(header_frame, text="8-Puzzle Solver",
                 font=(self.font_family, 24, "bold"),
                 bg=self.bg_color, fg=self.primary_color).pack()

        tk.Label(header_frame, text="using Uniform Cost Search (UCS)",
                 font=(self.font_family, 12),
                 bg=self.bg_color, fg=self.text_color_sub).pack(pady=(5, 0))

        grid_border_frame = tk.Frame(self.root, bg="#DDDDDD", bd=1)
        grid_border_frame.pack(pady=20)

        grid_frame = tk.Frame(grid_border_frame, bg=self.blank_tile_color, padx=5, pady=5)
        grid_frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(grid_frame, text="",
                                font=(self.font_family, 32, "bold"),
                                width=4, height=1,
                                relief="flat", bd=0, takefocus=False)
                btn.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                self.buttons[i][j] = btn
            grid_frame.grid_columnconfigure(i, weight=1)
            grid_frame.grid_rowconfigure(i, weight=1)

        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(pady=15, padx=20, fill="x")

        self.status_label = tk.Label(status_frame,
                                     text="Trạng thái ban đầu. Hãy bấm 'Giải'!",
                                     font=(self.font_family, 13, "bold"),
                                     bg=self.bg_color, fg=self.text_color_main,
                                     wraplength=400, justify="center")
        self.status_label.pack()

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=(20, 30))

        self.solve_btn = tk.Button(btn_frame, text="Giải",
                                   font=(self.font_family, 14, "bold"),
                                   bg=self.primary_color, fg="white",
                                   padx=20, pady=10, relief="flat", bd=0,
                                   activebackground="#0056b3", activeforeground="white",
                                   command=self.start_solving)
        self.solve_btn.grid(row=0, column=0, padx=15)
        self.reset_btn = tk.Button(btn_frame, text="Reset",
                                   font=(self.font_family, 14, "bold"),
                                   bg=self.error_color, fg="white",
                                   padx=20, pady=10, relief="flat", bd=0,
                                   activebackground="#c32a21", activeforeground="white",
                                   command=self.reset_board)
        self.reset_btn.grid(row=0, column=1, padx=15)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                val = self.current_state[i][j]
                if val == 0:
                    self.buttons[i][j].config(text="", bg=self.blank_tile_color, state="disabled")
                else:
                    self.buttons[i][j].config(text=str(val),
                                              bg=self.tile_color, fg=self.tile_text_color,
                                              state="normal")

    def reset_board(self):
        self.current_state = copy.deepcopy(start)
        self.update_board()
        self.status_label.config(text="Đã khôi phục trạng thái ban đầu.", fg=self.text_color_main)
        self.solve_btn.config(state="normal", bg=self.primary_color)
        self.reset_btn.config(state="normal", bg=self.error_color)

    def start_solving(self):
        if states_equal(self.current_state, goal):
            messagebox.showinfo("Thông báo", "Bảng đã ở trạng thái đích (GOAL) rồi!")
            return

        self.solve_btn.config(state="disabled", bg="#999999")
        self.reset_btn.config(state="disabled", bg="#999999")
        self.status_label.config(text="Thuật toán UCS đang tìm đường, vui lòng đợi...",
                                 fg=self.primary_color)
        self.root.update()

        path, cost_found = ucs(self.current_state, goal)

        if path is not None:
            self.status_label.config(
                text=f"Đã tìm ra đường! Đang mô phỏng {len(path)} bước...",
                fg=self.primary_color)
            self.animate_solution(path, cost_found)
        else:
            self.status_label.config(text="Không tìm thấy lời giải cho trạng thái này!",
                                     fg=self.error_color)
            self.solve_btn.config(state="normal", bg=self.primary_color)
            self.reset_btn.config(state="normal", bg=self.error_color)

    def animate_solution(self, path, cost_found):
        current_puzzle = copy.deepcopy(self.current_state)

        def step(index):
            if index < len(path):
                action = path[index]
                x, y = tim_o_trong(current_puzzle)
                nx, ny = move(x, y, action)
                current_puzzle[x][y], current_puzzle[nx][ny] = \
                    current_puzzle[nx][ny], current_puzzle[x][y]

                self.current_state = copy.deepcopy(current_puzzle)
                self.update_board()
                self.status_label.config(
                    text=f"Bước {index + 1}/{len(path)}: Di chuyển ô trống sang {action}",
                    fg=self.primary_color)
                self.root.after(600, step, index + 1)
            else:
                self.status_label.config(
                    text=f"Giải xong! {len(path)} bước với tổng Cost = {cost_found}. (GOAL) ✓",
                    fg=self.success_color)
                self.solve_btn.config(state="normal", bg=self.primary_color)
                self.reset_btn.config(state="normal", bg=self.error_color)

        step(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()