from enums import eTile
from collections import deque

gameEndingMoves = {}
hexDirections = [(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)]
queue = deque()
visited = set()
def eval(player, state, islands, isEndFunc):
    score = 0
    boardN = len(state)
    boardM = len(state[0])

    for island in islands:
        islandR, islandC = islands[island][0][0]
        owner = islands[island][1]
        targetR, targetC = boardN - islandR, boardM - islandC

        visited.clear()
        queue.clear()
        queue.append((islandR, islandC))
        visited.add((islandR, islandC))

        while queue:
            r, c = queue.popleft()
            for dr, dc in hexDirections:
                nr, nc = r + dr, c + dc
                if 0 <= nr < boardN and 0 <= nc < boardM:
                    if (nr, nc) not in visited and state[nr][nc] == owner:
                        visited.add((nr, nc))
                        queue.append((nr, nc))

        bestDistance = float("inf")
        for r, c in visited:
            dist = abs(r - targetR) + abs(c - targetC)
            if dist < bestDistance:
                bestDistance = dist

        if owner == player:
            score += bestDistance
        else:
            score -= bestDistance

    return score

def availableMoves(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == eTile.Playable.value[0]:
                yield (row, col)

def minValue(state, depth, alpha, beta, xPlayer, oPlayer, islands, isEndFunc, turn = None):
    iE, _ = isEndFunc(state, oPlayer)
    if iE:
        return (turn, -10001)
    
    moves = list(availableMoves(state))

    if depth in gameEndingMoves:
        gameEndingMove = gameEndingMoves[depth]
        if gameEndingMove in moves:
            moves.remove(gameEndingMove)
            moves.insert(0, gameEndingMove)

    if depth == 0:
        return(turn, eval(oPlayer, state, islands, isEndFunc))
    
    for m in moves:
        row, col = m
        state[row][col] = oPlayer
        beta = min(beta, maxValue(state, depth - 1, alpha, beta, xPlayer, oPlayer, islands, isEndFunc, m if turn is None else turn), key = lambda x: x[1])
        state[row][col] = eTile.Playable.value[0]
        if beta[1] <= alpha[1]:
            gameEndingMoves[depth] = m
            return beta
        
    return beta

def maxValue(state, depth, alpha, beta, xPlayer, oPlayer, islands, isEndFunc, turn = None):
    iE, _ = isEndFunc(state, xPlayer)
    if iE:
        return (turn, 10001)
    
    moves = list(availableMoves(state))

    if depth in gameEndingMoves:
        gameEndingMove = gameEndingMoves[depth]
        if gameEndingMove in moves:
            moves.remove(gameEndingMove)
            moves.insert(0, gameEndingMove)

    if depth == 0:
        return(turn, eval(xPlayer, state, islands, isEndFunc))
    
    for m in moves:
        row, col = m
        state[row][col] = xPlayer
        alpha = max(alpha, minValue(state, depth - 1, alpha, beta, xPlayer, oPlayer, islands, isEndFunc, m if turn is None else turn), key = lambda x: x[1])
        state[row][col] = eTile.Playable.value[0]
        if alpha[1] >= beta[1]:
            gameEndingMoves[depth] = m

            if depth == 3 and alpha[0] == None:
                alpha = (m, alpha[1])

            return alpha
        
    if depth == 3 and alpha[0] == None:
        alpha = (moves[0], alpha[1])

    return alpha

def minimax(board, xPlayer, oPlayer, islands, isEndFunc, alpha=(None, -10000), beta=(None, 10000)):
    gameEndingMoves.clear()
    return maxValue(board, 3, alpha, beta, xPlayer, oPlayer, islands, isEndFunc)

def performBotMove(board, botPlayer, islands, isEndFunc):
    boardCopy = [row[:] for row in board]
    humanPlayer = eTile.Player1.value[0] if botPlayer != eTile.Player1.value[0] else eTile.Player2.value[0]
    turn, _ = minimax(boardCopy, botPlayer, humanPlayer, islands, isEndFunc)
    return turn