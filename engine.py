from figures import pawn, knight, bishop, rook, king, queen
def is_valid_move(map, start, goal, figure):
    s_c, s_r = start
    g_c, g_r = goal
    goal_field = map[g_r][g_c]  # Korrigiert: erst Reihe, dann Spalte

    # Überprüfe, ob das Ziel innerhalb des Spielfelds liegt
    if not (0 <= g_c < 8 and 0 <= g_r < 8):
        return False

    # Überprüfe, ob die Figur am Startfeld existiert
    if map[s_r][s_c] != figure:
        return False

    # Überprüfe, ob das Ziel nicht von einer eigenen Figur besetzt ist
    if goal_field != "." and ((figure.isupper() and goal_field.isupper()) or (figure.islower() and goal_field.islower())):
        return False

    # Rufe die entsprechende Bewegungsfunktion basierend auf der Figur auf
    if figure.lower() == "p":
        return pawn(map, start, goal, figure)
    elif figure.lower() == "r":
        return rook(map, start, goal)
    elif figure.lower() == "n":
        return knight(map, start, goal)
    elif figure.lower() == "b":
        return bishop(map, start, goal)
    elif figure.lower() == "q":
        return queen(map, start, goal)
    elif figure.lower() == "k":
        return king(map, start, goal)

    return False