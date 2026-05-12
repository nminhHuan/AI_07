import random

def p_moves(x,y):
    moves=[]
    if x < 3:
        moves.append('D')
    if x > 0:
        moves.append('U')
    if y < 3:
        moves.append('R')
    if y > 0:
        moves.append('L')
    return moves

def move(x,y,action):
    if action == 'D':
        x+=1
    if action == 'U':
        x-=1
    if action == 'R':
        y+=1
    if action =='L':
        y-=1
    return x,y

def check_matrix(matrix):
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 1:
                return False
    return True

if __name__=='__main__':
    matrix=[]
    vi_tri=[]
    for i in range(4):
        row =list(map(int,input().split()))
        matrix.append(row)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j]==1:
                vi_tri.append((i,j))
    x,y=random.choice(vi_tri)
    print(f"vị trí ban đầu của máy hút bụi: ({x},{y})")
    while not(check_matrix(matrix)):
        action=''

        if matrix[x][y]==1:
            matrix[x][y]=0
            moves = p_moves(x,y)
            action = random.choice(moves)
            x,y= move(x,y,action)

        if matrix[x][y]==0:
            moves = p_moves(x,y)
            action = random.choice(moves)
            x,y= move(x,y,action)
        print(action)
        for i in matrix:
            print(i)
        print()