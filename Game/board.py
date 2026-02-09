from enums import eTile
from tableCreator import createTable
import customtkinter
from PIL import Image
from botController import performBotMove

def openView(m, isbot, playerfirst, mainapp, currentTheme, hidebuttons):
    global n, isBot, buttons, matrix, player1First, mainApp, lastMove, app, players, playerColors, currentPlayer, hideButtons
    n = int(m)
    isBot = isbot
    buttons = []
    matrix = []
    player1First = playerfirst
    lastMove = None
    mainApp = mainapp
    hideButtons = hidebuttons
    currentPlayer = 0 if player1First else 1 
    players = (eTile.Player1.value[0], eTile.Player2.value[0])
    playerColors = ('#B92020', '#4BC02A')

    customtkinter.set_appearance_mode(currentTheme)
    customtkinter.set_default_color_theme('dark-blue')

    app = customtkinter.CTkToplevel()
    app.protocol("WM_DELETE_WINDOW", exitClick)
    app.geometry("1280x720")
    app.title("Atoll")
    app.grid_columnconfigure(0, weight=2)
    app.grid_columnconfigure(1, weight=10)
    app.grid_rowconfigure(0, weight=1)

    startPage()
    app.mainloop()

hexDirections = [(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)]
def createGraphs(matrix, matrixN, matrixM):
    groups = {}
    currentGroup = 1
    processed = set()

    directions = [(1, -1), (2, 0), (1, 1)]
    
    for i in range(matrixN):
        for j in range(matrixM):
            if matrix[i][j] in [eTile.Invalid.value[0], eTile.Playable.value[0]] or (i, j) in processed:
                continue

            currentTile = matrix[i][j]
            processed.add((i, j))
            group = [(i, j)]

            for di, dj in directions:
                ni = i + di
                nj = j + dj
                while 0 <= ni < matrixN and 0 <= nj < matrixM:
                    if matrix[ni][nj] != currentTile:
                        break

                    processed.add((ni, nj))
                    group.append((ni, nj))
                    ni += di
                    nj += dj

            groups[currentGroup] = (group, currentTile)
            currentGroup += 1
            
    return groups

def dfs(board, x, y, oldTile, newTile):
    if (x < 0 or x >= len(board) or
        y < 0 or y >= len(board[0]) or
        board[x][y] != oldTile):
        return
    
    board[x][y] = newTile
    for hdi, hdj in hexDirections:
        dfs(board, x+hdi, y+hdj, oldTile, newTile)

def getConnectedGroups(group, board):
    res = [group]
    for curGroup in groups:
        if groups[curGroup][1] != groups[group][1] or curGroup == group:
            continue

        x, y = groups[curGroup][0][0]
        if board[x][y] != eTile.Connected.value[0]:
            continue

        res.append(curGroup)

    return res

def isGameFinished(board, curPlayer = None):
    processedGroups = set()

    if curPlayer is None:
        curPlayer = players[currentPlayer]

    for group in groups:
        ni, nj = groups[group][0][0]
        player = board[ni][nj]
        if player != curPlayer or group in processedGroups:
            continue

        boardCopy = [row[:] for row in board]
        dfs(boardCopy, ni, nj, player, eTile.Connected.value[0])
        processedGroups.add(group)
        
        connectedGroups = getConnectedGroups(group, boardCopy)
        lowest = iterateThroughGroups(connectedGroups, boardCopy)

        for conGroup in connectedGroups:
            processedGroups.add(conGroup)
        
        if lowest >= len(groups) / 2 + 1:
            return (True, boardCopy)
        
    return (False, [])

def getOrderedGroups():
    orderedGroups = [1]
    groupAmount = len(groups)
    orderedGroups.extend(range(2, groupAmount + 1, 2))
    orderedGroups.extend(range(groupAmount - 1, 2, -2))

    return orderedGroups, orderedGroups[::-1]

def processGroup(orderedGroups, board):
    currentIslandCount = 0
    finalIslandCount = 0

    for group in orderedGroups:
        currentIslandCount += 1
        x, y = groups[group][0][0]

        if board[x][y] == eTile.Connected.value[0]:
            finalIslandCount = currentIslandCount

    return finalIslandCount

def iterateThroughGroups(connectedGroups, board):
    lowest = -1
    orderedGroups, reverseOrderGroups = getOrderedGroups()
    for connectedGroup in connectedGroups:
        startIndex = orderedGroups.index(connectedGroup)
        reverseStartIndex = reverseOrderGroups.index(connectedGroup)

        firstOrderedGroups = orderedGroups[startIndex:] + orderedGroups[:startIndex]
        reverseOrderGroups = reverseOrderGroups[reverseStartIndex:] + reverseOrderGroups[:reverseStartIndex]
        curLowest = min(processGroup(firstOrderedGroups, board), processGroup(reverseOrderGroups, board))
        if lowest == -1:
            lowest = curLowest
            
        lowest = min(lowest, curLowest)
    
    return lowest

def isGameDraw():
    for row in matrix:
        if eTile.Playable.value[0] in row:
            return False

    return True

def botMove():
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            if matrix[i][j] == eTile.Playable.value[0]:
                buttons[i][j].configure(state = 'disabled')

    row, col =  performBotMove(matrix, players[currentPlayer], groups, isGameFinished)
    on_tile_click(row, col)

    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            if matrix[i][j] == eTile.Playable.value[0]:
                buttons[i][j].configure(state = 'normal')

def startPage():
    global buttons
    global matrix
    global groups
    matrix, matrixN, matrixM = createTable(n)
    groups = createGraphs(matrix, matrixN, matrixM)

    infoFrame = customtkinter.CTkFrame(app, fg_color="transparent")
    infoFrame.grid(row = 0, column = 0, sticky='nwse')
    infoFrame.grid_columnconfigure(0, weight=1)

    infoFrameFill(infoFrame)

    board_frame = customtkinter.CTkFrame(app, border_color='#000', border_width=1)
    board_frame.grid(row = 0, column = 1, sticky='nwse', padx=10, pady=10)
    board_frame.grid_rowconfigure(0, weight=1)
    board_frame.grid_columnconfigure(0, weight=1)

    boardHolder = customtkinter.CTkFrame(board_frame, fg_color='transparent')
    boardHolder.grid(row = 0, column = 0, padx = 10, pady = 10, sticky='nswe')

    for i in range(matrixN):
        boardHolder.grid_rowconfigure(i, weight=1)

    for i in range(matrixM):
        boardHolder.grid_columnconfigure(i, weight=1)

    buttons = render_board(boardHolder, matrix, matrixN, matrixM)
    if getCurrentPlayerName() == 'Bot':
        botMove()

def getCurrentPlayerName():
    if(players[currentPlayer] == eTile.Player1.value[0]):
        return 'Player 1'
    elif(isBot):
        return 'Bot'
    else:
        return 'Player 2'

def getCurrentPlayer():
    return f"Trenutni igrac: {getCurrentPlayerName()}"

def undoClick():
    global lastMove

    buttons[lastMove[0]][lastMove[1]].configure(fg_color = 'transparent', state='normal')
    matrix[lastMove[0]][lastMove[1]] = eTile.Playable.value[0]
    undoButton.configure(state = 'disabled')
    confirmButton.configure(state = 'disabled')
    lastMove = None

def confirmClick():
    global currentPlayerLabel, lastMove, currentPlayer, n
    print(f"{getCurrentPlayerName()} je odigrao: {chr(ord('A') - 1 + lastMove[1])} {(lastMove[0] + lastMove[1] - n + 1)//2}\n")
    status, board = isGameFinished(matrix)

    confirmButton.configure(state = 'disabled')
    undoButton.configure(state = 'disabled')

    if status == True or isGameDraw():
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == eTile.Connected.value[0]:
                    buttons[i][j].configure(fg_color = 'blue')
                if buttons[i][j] is not None:
                    buttons[i][j].configure(state = 'disabled')
                    if status != True:
                        buttons[i][j].configure(fg_color = 'yellow')

        print(f'Pobeda igraca: {getCurrentPlayerName()}' if status == True else 'Igra je neresena')
        if status == True:
            currentPlayerLabel.configure(text = f'Pobeda igraca: {getCurrentPlayerName()}', text_color= 'blue')
        else:
            currentPlayerLabel.configure(text = 'Igra je neresena', text_color= 'yellow')
    else:
        currentPlayer = (currentPlayer + 1) % 2
        lastMove = None
        currentPlayerLabel.configure(text = getCurrentPlayer(), text_color= playerColors[currentPlayer])
        if getCurrentPlayerName() == 'Bot':
            botMove()

def exitClick():
    app.withdraw()
    app.quit()
    mainApp.deiconify()

def changeAppTheme():
    customtkinter.set_appearance_mode("dark" if customtkinter.get_appearance_mode().lower() == "light" else "light")

def infoFrameFill(frame):
    global confirmButton, undoButton, currentPlayerLabel

    helperFrame = customtkinter.CTkFrame(frame, fg_color="transparent")
    helperFrame.grid(row = 0, column = 0, sticky='ew')
    helperFrame.grid_rowconfigure(0, weight=1) 
    helperFrame.grid_columnconfigure(0, weight=1) 

    currentPlayerLabel = customtkinter.CTkLabel(helperFrame, text=getCurrentPlayer(), font=('', 20), text_color= playerColors[currentPlayer])
    currentPlayerLabel.grid(row = 0, column = 0, padx = 20, pady = 20, sticky='w')

    theme_icon = customtkinter.CTkImage(
        light_image=Image.open("./assets/light_theme.png"),
        dark_image=Image.open("./assets/dark_theme.png"),
        size=(40, 40)
    )

    themeButton = customtkinter.CTkButton(
        helperFrame,
        text="",
        width=40,
        height=40,
        hover=None,
        fg_color='transparent',
        border_width=0,
        image=theme_icon,
        command=changeAppTheme
    )
    themeButton.grid(row=0, column=1, padx=10, pady=10, sticky='nwse')

    buttonsFrame = customtkinter.CTkFrame(frame, fg_color='transparent')
    buttonsFrame.grid(row = 1, column = 0, padx = 20, pady = 20, sticky='we')
    buttonsFrame.grid_columnconfigure(0, weight=1)
    buttonsFrame.grid_columnconfigure(1, weight=1)
    buttonsFrame.grid_rowconfigure(0, weight=1)

    confirmIcon = Image.open('./assets/checkLight.png')
    undoIcon = Image.open('./assets/undoLight.png')
    cancelIcon = Image.open('./assets/cancelLight.png')

    confirmButton = customtkinter.CTkButton(buttonsFrame, text='Confirm', state='disabled', command=confirmClick, image=customtkinter.CTkImage(light_image=confirmIcon, size=(24, 24)))
    confirmButton.grid(row = 0, column = 0, sticky='nswe', pady=10, padx=(0, 5))

    undoButton = customtkinter.CTkButton(buttonsFrame, text='Undo', state='disabled', command=undoClick, image=customtkinter.CTkImage(light_image=undoIcon, size=(24, 24)))
    undoButton.grid(row = 0, column = 1, sticky='nswe', pady=10, padx=(5, 0))

    if hideButtons:
        confirmButton.grid_forget()
        undoButton.grid_forget()

    exitButton = customtkinter.CTkButton(buttonsFrame, text='Exit', command=exitClick, image=customtkinter.CTkImage(light_image=cancelIcon, size=(18, 18)))
    exitButton.grid(row = 1, column = 0, sticky='we', columnspan = 2, pady=10)


def create_button(parent, tile, row, col):
    if tile == eTile.Playable.value[0]:
        fg = "transparent"
        state = "normal"
    elif tile == eTile.Player1.value[0]:
        fg = playerColors[0]
        state = "disabled"
    elif tile == eTile.Player2.value[0]:
        fg = playerColors[1]
        state = "disabled"

    btn = customtkinter.CTkButton(
        parent,
        text='',
        corner_radius=30,
        width=30,
        fg_color=fg,
        border_width=2,
        border_color=("#000", "#bab2b2"),
        state=state,
        command=lambda: on_tile_click(row, col)
    )

    btn.grid(row=row, column=col)
    return btn

def render_board(parent, matrix, rows, cols):
    buttons = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if(matrix[i][j] == eTile.Invalid.value[0]):
                continue

            buttons[i][j] = create_button(parent, matrix[i][j], i, j)

    return buttons

def on_tile_click(r, c):
    global lastMove, currentPlayer

    if matrix[r][c] != eTile.Playable.value[0]:
        return
    
    if lastMove != None:
        buttons[lastMove[0]][lastMove[1]].configure(fg_color = 'transparent', state='normal')
        matrix[lastMove[0]][lastMove[1]] = eTile.Playable.value[0]

    lastMove = (r, c)
    undoButton.configure(state = 'normal')
    confirmButton.configure(state = 'normal')
    matrix[r][c] = players[currentPlayer]
    buttons[r][c].configure(fg_color = playerColors[currentPlayer], state='disabled')
    if hideButtons or getCurrentPlayerName() == 'Bot':
        confirmClick()
    else:
        print(f"{getCurrentPlayerName()} je odabrao: {chr(ord('A') - 1 + c)} {(r + c - n + 1)//2}")