import curses
import math
import mapgen_01 as mapgen

gen = mapgen.Generator()
gen.gen_level()
gen.gen_tiles_level()
room_list = gen.room_list
corridor_list = gen.corridor_list

# Sample room and corridor definitions (these come from the dungeon generator)
'''
room_list = [
    [45, 26, 7, 9], [29, 18, 8, 10], [21, 28, 9, 5], [7, 26, 7, 7], [21, 16, 9, 7],
    [18, 51, 9, 6], [42, 52, 6, 9], [4, 46, 9, 5], [20, 4, 8, 6], [56, 1, 7, 10],
    [16, 5, 7, 7], [55, 34, 7, 9], [37, 33, 7, 9], [8, 11, 6, 8], [34, 2, 6, 8]
]
'''
'''
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
    Generates a 2D grid (list of lists) representing the dungeon.
    Walls are '#' and floors are '.'. The grid covers all rooms
    and corridors, with the offset computed so that the grid indices
    start at 0.
    """
    # Determine boundaries from rooms and corridors.
    min_x = float('inf')
    min_y = float('inf')
    max_x = 0
    max_y = 0

    for room in room_list:
        x, y, w, h = room
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w - 1)
        max_y = max(max_y, y + h - 1)

    for corridor in corridor_list:
        for (cx, cy) in corridor:
            min_x = min(min_x, cx)
            min_y = min(min_y, cy)
            max_x = max(max_x, cx)
            max_y = max(max_y, cy)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Create grid filled with walls.
    grid = [['#' for _ in range(width)] for _ in range(height)]

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
        for i in range(len(corridor) - 1):
            (x1, y1) = corridor[i]
            (x2, y2) = corridor[i + 1]
            if y1 == y2:
                # Horizontal corridor.
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y1 - min_y][x - min_x] = '.'
            elif x1 == x2:
                # Vertical corridor.
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y - min_y][x1 - min_x] = '.'
            else:
                # Diagonal corridors (if applicable) can be added here.
                pass

    return grid, min_x, min_y


def main(stdscr):
    curses.curs_set(0)  # Hide the cursor.
    stdscr.nodelay(False)  # Wait for user input.
    stdscr.keypad(True)  # Enable arrow key detection.

    # Generate dungeon grid.
    grid, offset_x, offset_y = generate_dungeon_map(room_list, corridor_list)
    grid_height = len(grid)
    grid_width = len(grid[0])

    # Fixed viewport radius.
    radius = 5  # This creates a (2*radius+1) x (2*radius+1) window.

    # Place player in the center of the first room.
    first_room = room_list[0]
    player_x = first_room[0] + first_room[2] // 2 - offset_x
    player_y = first_room[1] + first_room[3] // 2 - offset_y

    while True:
        stdscr.clear()

        # Instead of clipping the viewport to the grid bounds,
        # we iterate over a fixed window centered on the player.
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                tile_x = player_x + dx
                tile_y = player_y + dy

                # Calculate relative distance for a "torch" effect.
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > radius:
                    ch = ' '  # Outside the torchlight.
                else:
                    # If the tile lies outside the grid boundaries,
                    # draw a wall; otherwise, show the grid's character.
                    if (tile_x < 0 or tile_x >= grid_width or
                            tile_y < 0 or tile_y >= grid_height):
                        ch = '#'
                    else:
                        ch = grid[tile_y][tile_x]

                # Player is always drawn at the center of the viewport.
                if dx == 0 and dy == 0:
                    ch = '@'

                # Draw the tile relative to the fixed viewport.
                try:
                    stdscr.addch(dy + radius, dx + radius, ch)
                except curses.error:
                    pass

        stdscr.refresh()

        # Handle user input for movement.
        key = stdscr.getch()
        new_x, new_y = player_x, player_y
        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1
        elif key == ord('q'):
            break

        # Ensure the new position is within grid bounds and is a floor tile.
        if (0 <= new_x < grid_width and 0 <= new_y < grid_height
                and grid[new_y][new_x] == '.'):
            player_x, player_y = new_x, new_y


curses.wrapper(main)
