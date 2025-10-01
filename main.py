from map import create_map,print_map,field_to_index
from engine import is_valid_move, make_move

def chess():
    map = create_map()  # Funktion aufrufen mit ()
    player = "white"

    while True:
        print_map(map)
        turn = input(f"{player}'s turn: ")
        if turn.lower() == "exit":
            break
        try:
            start_field, goal_field = turn.split()
            start = field_to_index(start_field)
            goal = field_to_index(goal_field)
            figure = map[start[0]][start[1]]
            if is_valid_move(map, start, goal, figure):
                map = make_move(map, start, goal)
                player = "black" if player == "white" else "white"
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter your move in the format 'e2 e4'.")
        except IndexError:
            print("Invalid field. Please use fields from a1 to h8.")

if __name__ == "__main__":
    chess()
