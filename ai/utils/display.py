from os import system

def display(board, position=(), clear=True):
    if clear: system('clear')
    string = []
    for i in range(len(board)):
        string.append([])
        for j in range(len(board[i])):
            string[i].append("." if board[i][j].state == 0 else "o" if board[i][j].state == 1 else "x")
    for point in position:
        string[point[0]][point[1]] = "*"
    for i in string:
        print("".join(i))
