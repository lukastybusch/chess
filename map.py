def create_map():
    map = [
        ["r","n","b","q","k","b","n","r"],  
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]
    return map

def print_map(map):
    print("  a b c d e f g h")
    for i, row in enumerate(map):
        print(8-i," ".join(row), 8-i)
    print("  a b c d e f g h")

def field_to_index(field):
    column = ord(field[0])-ord("a")
    row = 8 - int(field[1])
    return row, column
