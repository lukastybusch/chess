def pawn(map, start, goal, figure):
    s_r, s_c = start  # start = (row, column) von field_to_index
    g_r, g_c = goal   # goal = (row, column) von field_to_index
    goal_field = map[g_r][g_c]

    direction = 1 if figure.islower() else -1  # schwarz: +1 (nach unten), weiß: -1 (nach oben)
    
    # moving forward
    if s_c == g_c and goal_field == ".":
        if g_r - s_r == direction:
            return True
        
        # first move (2steps)
        if figure.isupper() and s_r == 6 and g_r == 4 and goal_field == ".":
            return True
        if figure.islower() and s_r == 1 and g_r == 3 and goal_field == ".":
            return True
    
    # hit (diagonal attack)
    if abs(g_c - s_c) == 1 and g_r - s_r == direction and goal_field != ".":
        return True
    
    return False

def rook(map, start, goal):
    s_r, s_c = start  # start = (row, column)
    g_r, g_c = goal   # goal = (row, column)

    # Der Turm bewegt sich nur horizontal oder vertikal
    if s_c != g_c and s_r != g_r:
        return False
    
    # Horizontal bewegung (gleiche Reihe)
    if s_r == g_r:
        step = 1 if g_c > s_c else -1
        # Überprüfe alle Felder zwischen Start und Ziel (exklusive)
        for c in range(s_c + step, g_c, step):
            if map[s_r][c] != ".":
                return False
        return True
    
    # Vertikale Bewegung (gleiche Spalte)
    elif s_c == g_c:
        step = 1 if g_r > s_r else -1
        # Überprüfe alle Felder zwischen Start und Ziel (exklusive)
        for r in range(s_r + step, g_r, step):
            if map[r][s_c] != ".":
                return False
        return True
    
    return False

def king(map, start, goal):
    s_r, s_c = start  # start = (row, column)
    g_r, g_c = goal   # goal = (row, column)
    goal_field = map[g_r][g_c]
    
    # Der König kann sich nur ein Feld in jede Richtung bewegen
    col_diff = abs(g_c - s_c)
    row_diff = abs(g_r - s_r)
    
    # Überprüfe, ob die Bewegung nur ein Feld weit ist
    if col_diff <= 1 and row_diff <= 1 and (col_diff != 0 or row_diff != 0):
        # Der König kann auf ein leeres Feld ziehen oder eine gegnerische Figur schlagen
        return True
    
    return False

def knight(map, start, goal):
    s_r, s_c = start  # start = (row, column)
    g_r, g_c = goal   # goal = (row, column)

    col_diff = abs(g_c - s_c)
    row_diff = abs(g_r - s_r)

    # Der Springer bewegt sich in einem "L"-Muster: 2 Felder in eine Richtung und 1 Feld in die andere Richtung
    if (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2):
        return True
    
    return False

def bishop(map, start, goal):
    s_r, s_c = start  # start = (row, column)
    g_r, g_c = goal   # goal = (row, column)

    col_diff = abs(g_c - s_c)
    row_diff = abs(g_r - s_r)

    # Der Läufer bewegt sich diagonal, was bedeutet, dass die Differenz in Spalten und Reihen gleich sein muss
    if col_diff == row_diff:
        col_step = 1 if g_c > s_c else -1
        row_step = 1 if g_r > s_r else -1
        
        c, r = s_c + col_step, s_r + row_step
        while c != g_c and r != g_r:
            if map[r][c] != ".":
                return False
            c += col_step
            r += row_step
        return True
    
    return False

def queen(map, start, goal):
    # Die Dame kombiniert die Bewegungen von Turm und Läufer
    return rook(map, start, goal) or bishop(map, start, goal)

