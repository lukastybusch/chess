from map import create_map,print_map,field_to_index

def chess():
    map = create_map
    player = "white"

    while True:
        print_map(map)
        turn = input(f"{player}'s turn: ")