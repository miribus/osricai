import curses
import mapgen_01 as mapgen

gen = mapgen.Generator()
gen.gen_level()
gen.gen_tiles_level()
room_list = gen.room_list
corridor_list = gen.corridor_list
# These are the sample room and corridor lists, as found in the RogueBasin code.
'''
room_list = [
    [45, 26, 7, 9], [29, 18, 8, 10], [21, 28, 9, 5], [7, 26, 7, 7], [21, 16, 9, 7],
    [18, 51, 9, 6], [42, 52, 6, 9], [4, 46, 9, 5], [20, 4, 8, 6], [56, 1, 7, 10],
    [16, 5, 7, 7], [55, 34, 7, 9], [37, 33, 7, 9], [8, 11, 6, 8], [34, 2, 6, 8]
]

corridor_list = [
    [(37, 26), (44, 26)],
    [(29, 28), (29, 27)],
    [(14, 28), (20, 28)],
    [(11, 25), (11, 18), (20, 18)],
    [(24, 23), (24, 50)],
    [(27, 56), (41, 56)],
    [(13, 46), (46, 46), (46, 51)],
    [(6, 45), (6, 4), (19, 4)],
    [(28, 5), (55, 5)],
    [(23, 5), (55, 5)],
    [(20, 12), (20, 40), (54, 40)],
    [(44, 38), (54, 38)],
    [(14, 13), (40, 13), (40, 32)],
    [(14, 17), (37, 17), (37, 10)],
    [(30, 22), (62, 22), (62, 11)],
    [(37, 27), (37, 16)],
    [(14, 12), (57, 12), (57, 59)],
    [(6, 59), (6, 29), (44, 29)]
]
'''

def generate_dungeon_map(room_list, corridor_list):
    """
    Creates a 2D grid (list of lists) representing the dungeon.
    Initially, the grid is filled with walls ('#').
    Rooms and corridors are then “carved” out by replacing '#' with floor ('.').

    We first calculate the minimum and maximum coordinates to compute the grid's size,
    applying an offset to normalize the coordinate system.
    """
    # Initialize our boundaries.
    min_x = float('inf')
    min_y = float('inf')
    max_x = 0
    max_y = 0

    # Process room_list to determine min/max coordinates.
    for room in room_list:
        x, y, w, h = room
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w - 1)
        max_y = max(max_y, y + h - 1)

    # Process corridor_list (each corridor is a list of (x, y) points).
    for corridor in corridor_list:
        for (cx, cy) in corridor:
            min_x = min(min_x, cx)
            min_y = min(min_y, cy)
            max_x = max(max_x, cx)
            max_y = max(max_y, cy)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Create a 2D grid filled with walls.
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Carve out rooms.
    for room in room_list:
        rx, ry, rw, rh = room
        offset_x = rx - min_x
        offset_y = ry - min_y
        for j in range(rh):
            for i in range(rw):
                grid[offset_y + j][offset_x + i] = '.'

    # Carve out corridors.
    for corridor in corridor_list:
        # Each corridor can have 2 or 3 points (or more, if it bends several times).
        for i in range(len(corridor) - 1):
            (x1, y1) = corridor[i]
            (x2, y2) = corridor[i + 1]
            # If it's a horizontal corridor (y-value is constant):
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y1 - min_y][x - min_x] = '.'
            # If it's a vertical corridor (x-value is constant):
            elif x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y - min_y][x1 - min_x] = '.'
            else:
                # For a diagonal (if ever encountered), you could add additional logic.
                pass

    return grid, min_x, min_y


def main(stdscr):
    # Configure curses for a smoother experience.
    curses.curs_set(0)  # Hide the blinking cursor.
    stdscr.nodelay(False)  # Blocks waiting for user input.
    stdscr.keypad(True)  # Enable arrow key recognition.

    # Generate the dungeon grid and capture the offset.
    grid, offset_x, offset_y = generate_dungeon_map(room_list, corridor_list)
    grid_height = len(grid)
    grid_width = len(grid[0])

    # Place the player in the center of the first room.
    first_room = room_list[0]
    player_x = first_room[0] + first_room[2] // 2 - offset_x
    player_y = first_room[1] + first_room[3] // 2 - offset_y

    # Main game loop.
    while True:
        stdscr.clear()
        # Draw the dungeon.
        for y in range(grid_height):
            for x in range(grid_width):
                # If this tile is where the player is, draw '@'
                if x == player_x and y == player_y:
                    stdscr.addch(y, x, '@')
                else:
                    stdscr.addch(y, x, grid[y][x])
        stdscr.refresh()

        key = stdscr.getch()

        # Calculate the new potential player position.
        new_x, new_y = player_x, player_y
        if key == curses.KEY_UP:
            new_y = player_y - 1
        elif key == curses.KEY_DOWN:
            new_y = player_y + 1
        elif key == curses.KEY_LEFT:
            new_x = player_x - 1
        elif key == curses.KEY_RIGHT:
            new_x = player_x + 1
        elif key == ord('q'):
            # Press 'q' to quit the game.
            break

        # Check if the new position is within bounds and on a floor tile.
        if (0 <= new_x < grid_width and 0 <= new_y < grid_height) and (grid[new_y][new_x] == '.'):
            player_x, player_y = new_x, new_y


curses.wrapper(main)
