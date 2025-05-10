import curses
import math
import monsters  # Import the monster module you just created
import mapgen_01 as mapgen
import pathfinding
import player
import time
import statuslogs
import combat
import threedee
import error_handling



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


def main(stdscr):
    gen = mapgen.Generator(style="indoor")
    gen.gen_level()
    gen.gen_tiles_level()
    room_list = gen.room_list
    corridor_list = gen.corridor_list
    curses.curs_set(0)  # Hide cursor
    height, width = stdscr.getmaxyx()  # Get screen size

    # Define window sizes correctly
    dungeon_height = height - 12  # Leave space for combat log
    print(dungeon_height, "dheight")
    dungeon_width = width - 65  # Leave space for stats sidebar
    print(dungeon_width, "dwidth")
    stats_width = 20
    print(stats_width, "statsw")
    log_height = 10
    print(log_height, "logw")

    # ascii_3d_width = 20  # Width of the 3D window
    # ascii_3d_height = 10  # Height (same as combat log for symmetry)
    # print(ascii_3d_width, ascii_3d_height, "a3d")
    # ascii_3d_x = dungeon_width - 20  # Positioned next to 2D map
    # ascii_3d_y = 0  # Top of the screen

    # dbascii_3d_width = 20  # Width of the 3D window
    # dbascii_3d_height = 10  # Height (same as combat log for symmetry)
    # print(dbascii_3d_width, dbascii_3d_height, "dba3d")
    # dbascii_3d_x = dungeon_width - 40  # Positioned next to 2D map
    # dbascii_3d_y = 0  # Top of the screen


    # Create separate windows
    dungeon_win = curses.newwin(dungeon_height, dungeon_width, 0, 0)  # Dungeon viewport
    #dbascii_3d_win = curses.newwin(dbascii_3d_height, dbascii_3d_width, 0, dungeon_width+1)
    #ascii_3d_win = curses.newwin(ascii_3d_height, ascii_3d_width, 0, dungeon_width+dbascii_3d_width+2)
    stats_win = curses.newwin(height-1, stats_width, 0, dungeon_width+1)  # Sidebar
    combat_win = curses.newwin(log_height, dungeon_width, dungeon_height, 0)  # Combat log below dungeon



    playerone = player.Player("MyName")
    grid, offset_x, offset_y = generate_dungeon_map(room_list, corridor_list)
    grid_height, grid_width = len(grid), len(grid[0])

    #radius = 5  # Viewport size
    first_room = room_list[0]
    player_x = first_room[0] + first_room[2] // 2 - offset_x
    player_y = first_room[1] + first_room[3] // 2 - offset_y

    monster_data = monsters.load_monsters_from_json()
    try:
        monster_list = monsters.place_monsters(grid, room_list, monster_data)
    except:
        error_handling.pc_failure()
        input("PRESS ENTER TO CONTINUE")

    combat_log = []  # Combat event storage

    while True:
        time.sleep(.10)
        # Clear each window separately, **don't overwrite everything**
        dungeon_win.clear()
        stats_win.clear()
        combat_win.clear()



        dij_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y)
        monsters.move_toward_player(monster_list, dij_map, grid, player_x, player_y, combat_log)

        # **Draw dungeon viewport in its designated window**
        if gen.style == "indoor":
            for dy in range(-playerone.indoorsight, playerone.indoorsight + 1):
                for dx in range(-playerone.indoorsight, playerone.indoorsight + 1):
                    tile_x, tile_y = player_x + dx, player_y + dy
                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    if distance > playerone.indoorsight:
                        ch = ' '
                    elif tile_x < 0 or tile_x >= grid_width or tile_y < 0 or tile_y >= grid_height:
                        ch = '#'
                    else:
                        ch = grid[tile_y][tile_x]

                    for m in monster_list:
                        if m.x == tile_x and m.y == tile_y:
                            ch = m.char
                            break

                    if dx == 0 and dy == 0:
                        ch = '@'

                    dungeon_win.addch(dy + playerone.indoorsight, dx + playerone.indoorsight, ch)

        # Initialize facing direction
        player_facing = "south"  # Default direction at game start
        player_last = "south"

        # draw **3d window**  # This didn't ever work as planned, might go back to it later
        # ascii_3d_win.clear()
        # dbascii_3d_win.clear()
        # threedee.render_ascii_3d_view(ascii_3d_win, grid, player_x, player_y, view_distance=10, player_facing="south")
        # threedee.render_ascii_3d_debug(dbascii_3d_win, grid, player_x, player_y, view_distance=10, player_facing="south")

        # Draw **player stats in sidebar window**
        statuslogs.display_player(stats_win, playerone)

        # Draw **combat log below dungeon**
        statuslogs.display_combat_log(combat_win, combat_log)

        # Refresh all windows separately, **ensure order is correct**
        dungeon_win.refresh()
        stats_win.refresh()
        combat_win.refresh()
        # ascii_3d_win.refresh()
        # dbascii_3d_win.refresh()
        stdscr.refresh()  # Refresh main screen **last**

        # Handle movement
        key = stdscr.getch()
        new_x, new_y = player_x, player_y

        # Handle movement and directional updates
        key = stdscr.getch()
        if key == curses.KEY_UP:
            new_y -= 1
            # player_facing = "north"
        elif key == curses.KEY_DOWN:
            new_y += 1
            # player_facing = "south"
        elif key == curses.KEY_LEFT:
            new_x -= 1
            # player_facing = "west"
        elif key == curses.KEY_RIGHT:
            new_x += 1
            # player_facing = "east"
        elif key == ord(' '):  # SPACEBAR (null movement)
            pass  # Player stays in place, but keeps their last facing direction
        elif key == ord('q'):
            break

        # Only move if valid
        if 0 <= new_x < grid_width and 0 <= new_y < grid_height and grid[new_y][new_x] == '.':
            player_x, player_y = new_x, new_y

        # **Combat processing**

        combat.check_and_resolve_combat(monster_list, grid, player_x, player_y, playerone, combat_log, gen)

        # **Game Over Check**
        if playerone.health <= 0:
            combat_log.append("Game Over - You have died!")
            statuslogs.display_combat_log(combat_win, combat_log)
            combat_win.refresh()  # Refresh combat log one last time
            stdscr.getch()  # Pause before quitting
            break

def rungame():
    running = False
    while not running:
        try:
            curses.wrapper(main)
            running = True
        except curses.error:
            error_handling.pc_failure()
            input("")
