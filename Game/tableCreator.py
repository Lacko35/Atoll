from enums import eTile

def createEmptyTable(matrixN, matrixM):
    res = []
    for _ in range(matrixN):
        row = []
        for _ in range(matrixM):
            row.append(eTile.Invalid.value[0])
        res.append(row)
    return res

def fillEdgeValues(matrix, n, matrixN):
    for i in range(1, n):
        p1 = eTile.Player2.value[0] if i < n/2 else eTile.Player1.value[0]
        p2 = eTile.Player1.value[0] if i < n/2 else eTile.Player2.value[0]
        matrix[i - 1][n - i] = p1
        matrix[matrixN - i][n + i] = p1
        matrix[i - 1][n + i] = p2
        matrix[matrixN - i][n - i] = p2
        for j in range(n - i + 2, n + i - 1, 2):
            matrix[i - 1][j] = eTile.Playable.value[0]
            matrix[matrixN - i][j] = eTile.Playable.value[0]
            
    for i in range(2, n * 2 - 1, 2):
        matrix[n-1][i] = eTile.Playable.value[0]
        matrix[matrixN-n][i] = eTile.Playable.value[0]
    return matrix

def fillSeparator(matrix, n, m):
    for i in range(1, n*2, 2):
        matrix[m][i] = eTile.Playable.value[0]
    return matrix

def fillMiddleValues(matrix, n):
    matrix = fillSeparator(matrix, n, n)
    crnt = 1
    for i in range(n+1, (n+1)*2+(n-4), 2):
        p1 = eTile.Player2.value[0] if crnt < n/2 else eTile.Player1.value[0]
        p2 = eTile.Player1.value[0] if crnt < n/2 else eTile.Player2.value[0]
        matrix[i][0] = p1
        matrix[i][n*2] = p2
        for j in range(2, n*2-1, 2):
            matrix[i][j] = eTile.Playable.value[0]
        matrix = fillSeparator(matrix, n, i+1)
        crnt+=1

    return matrix

def fillTable(matrix, n, matrixN):
    matrix = fillEdgeValues(matrix, n, matrixN)
    matrix = fillMiddleValues(matrix, n)
    return matrix

def createTable(n):
    matrixN = n * 4 - 1
    matrixM = n * 2 +1
    matrix = createEmptyTable(matrixN, matrixM)
    matrix = fillTable(matrix, n, matrixN)
    return matrix, matrixN, matrixM