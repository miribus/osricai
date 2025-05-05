import curses
import math
import monsters  # Import the monster module you just created
import mapgen_01 as mapgen
import pathfinding
import player

gen = mapgen.Generator()
gen.gen_level()
gen.gen_tiles_level()
room_list = gen.room_list
corridor_list = gen.corridor_list


def generate_dungeon_map(room_list, corridor_list):
    """
    Generates a 2D grid representing the dungeon.
    Walls are '#' and floors are '.'. Computes an offset so that
    the grid indices start at 0.
    """
    # Determine the boundaries of the dungeon.
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

    # Create a grid filled with walls.
    grid = [['#' for _ in range(width)] for _ in range(height)]

    # Carve out each room.
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
            (x2, y2) = corridor[i+1]
            # Horizontal corridor.
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y1 - min_y][x - min_x] = '.'
            # Vertical corridor.
            elif x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y - min_y][x1 - min_x] = '.'
            else:
                # If diagonal corridors occur, additional logic would be needed.
                pass

    return grid, min_x, min_y

def draw_player_stats(stats_win, player):
    """Render player stats in a separate window."""
    stats_win.clear()
    stats_win.box()  # Draws a border around the stats window
    stats_win.addstr(1, 2, f"Player: {player.name}")
    stats_win.addstr(2, 2, f"HP: {player.health}")
    stats_win.addstr(3, 2, f"STR: {player.strength}")
    stats_win.addstr(4, 2, f"DEX: {player.dexterity}")
    stats_win.addstr(5, 2, f"CON: {player.constitution}")
    stats_win.refresh()

def draw_dungeon(dungeon_win, grid):
    """Render dungeon map in the main window."""
    dungeon_win.clear()
    for y, row in enumerate(grid):
        dungeon_win.addstr(y, 0, ''.join(row))
    dungeon_win.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor

    # Define window sizes
    height, width = stdscr.getmaxyx()
    dungeon_height = height
    dungeon_width = width - 20  # Leave space for stats HUD

    # Create windows
    dungeon_win = curses.newwin(dungeon_height, dungeon_width, 0, 0)
    stats_win = curses.newwin(dungeon_height, 20, 0, dungeon_width)

    # Example player and map
    playerone = player.Player(name="Barnabas", strength=16, dexterity=14, constitution=12, intelligence=15, wisdom=10, charisma=18, health=100)
    grid, min_x, min_y = generate_dungeon_map(room_list, corridor_list)  # Example empty dungeon

    # Main loop
    while True:
        draw_dungeon(dungeon_win, grid)
        draw_player_stats(stats_win, playerone)

        key = stdscr.getch()
        if key == ord("q"):  # Quit when 'q' is pressed
            break

curses.wrapper(main)
