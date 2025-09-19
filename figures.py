def pawn(map, start, goal, figure):
    s_c, s_r = start
    g_c, g_r = goal
    goal_field = map[g_c][g_r]

    direction = -1 if figure.islower() else 1
    # moving forward
    if s_c == g_c and goal_field == ".":
        if g_r - s_r == direction:
            return True
        
    # first move (2steps)
        if figure.isupper() and s_r == 6 and g_r == 4 and goal_field == ".":
            return True
        if figure.islower() and s_r == 1 and g_r == 3 and goal_field == ".":
            return True
    
    # hit
    if abs(g_c - s_c) == 1 and g_r-s_r == direction and goal_field != ".":
        return True
    
    return False

def rook(map, start, goal):
    s_c, s_r = start
    g_c, g_r = goal

    # horizontal
    if s_r == g_r:
        step = 1 if g_c > s_c else -1
        for c in range(s_c + step, g_c - step, step):
            if map[s_r][c] != ".":
                return False
        return True
    # vertical
    elif s_c == g_c:
        step = 1 if g_r > s_r else -1
        for r in range(s_r + step, g_r - step, step):
            if map[r][s_c] != ".":
                return False
        return True
    return False
