from collections import deque

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
                queue.append((xk, xi))
    return True

if __name__ == "__main__":
    partial_board = [
        1, 2, 3,
        4, -1, 6,
        7, -1, 0
    ]
    domains = {}
    for i, v in enumerate(partial_board):
        domains[i] = {v} if v != -1 else set(range(9))
    neighbors = {xi: neighbors_of(xi) for xi in VARS}
    print("=== BAN DAU ===")
    for r in range(3):
        print(*(partial_board[r * 3:r * 3 + 3]))
    print("-" * 15)
    consistent = ac3(domains, neighbors)
    if not consistent:
        print("CSP khong nhat quan")
    elif all(len(domains[i]) == 1 for i in VARS):
        board = [next(iter(domains[i])) for i in VARS]
        print("KET QUA")
        for r in range(3):
            print(*(board[r * 3:r * 3 + 3]))
        print("\nGOAL!")
    else:
        print("KET QUA")
        for i in VARS:
            print(f"X{i}: {sorted(domains[i])}")
        print("\nChua giai duoc het!")