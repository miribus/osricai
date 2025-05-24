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

levelmap = None  # Initialize levelmap variable
prev_key = None  # Store previous key

def handle_input(stdscr):
    global prev_key
    key = stdscr.getch()

    # Detect key release by checking for -1
    if key == -1:
        prev_key = None  # Reset only when no key is pressed
        return None

    if key == prev_key:
        return None  # Ignore repeated input while holding key

    prev_key = key  # Store new keypress
    return key


def main(stdscr):
    stdscr.nodelay(True)
    last_player_update = time.time()
    # last_monster_update = time.time()
    player_interval = 0.5  # Adjust this to slow down player movement
    # monster_interval = 0.5  # Adjust monster movement speed
    levelmap = mapgen.Generator(width=32, height=32, style="indoor")
    levelmap.gen_level()
    levelmap.gen_tiles_level()
    room_list = levelmap.room_list
    corridor_list = levelmap.corridor_list
    curses.curs_set(0)  # Hide cursor
    height, width = stdscr.getmaxyx()  # Get screen size

    # Define window sizes correctly
    dungeon_height = height - 12  # Leave space for combat log
    print(dungeon_height, "dheight")
    dungeon_width = width - 65  # Leave space for stats sidebar
    print(dungeon_width, "dwidth")
    stats_width = 20
    print(stats_width, "statsw")
    log_height = 12
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



    playerone = player.Player("MyName", classtype=4)
    grid, offset_x, offset_y = levelmap.generate_dungeon_map(room_list, corridor_list)
    grid_height, grid_width = len(grid), len(grid[0])

    #radius = 5  # Viewport size
    first_room = room_list[0]
    player_x = first_room[0] + first_room[2] // 2 - offset_x
    player_y = first_room[1] + first_room[3] // 2 - offset_y

    monster_data = monsters.load_monsters_from_json(grid=grid, levelmap=levelmap)
    monster_list = monsters.place_monsters(grid, room_list, monster_data)

    combat_log = []  # Combat event storage
    while True:

        time.sleep(0)
        # Clear each window separately, **don't overwrite everything**
        dungeon_win.clear()
        stats_win.clear()
        # combat_win.clear()

        dij_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y, levelmap=levelmap)

        # **Combat processing**
        combat.check_and_resolve_player_combat(monster_list, grid, player_x, player_y, playerone, combat_log, levelmap)

        for monster in monster_list:
            if monster.can_attack():
                monsters.move_toward_player(monster_list, dij_map, grid, player_x, player_y, combat_log, levelmap)
                combat.check_and_resolve_monster_combat(monster_list, grid, player_x, player_y, playerone, combat_log, levelmap)

        # **Draw dungeon viewport in its designated window**
        if levelmap.style == "indoor":
            for dy in range(-playerone.indoorsight, playerone.indoorsight + 1):
                for dx in range(-playerone.indoorsight, playerone.indoorsight + 1):
                    tile_x, tile_y = player_x + dx, player_y + dy
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    print("Generating tile at", tile_x, tile_y, "distance", distance)
                    if distance > playerone.indoorsight:
                        ch = levelmap.tiles["floor"]
                        print("Printing floor tile at", tile_x, tile_y)
                    elif tile_x < 0 or tile_x >= grid_width or tile_y < 0 or tile_y >= grid_height:
                        ch = levelmap.tiles["wall"]
                        print("Printing wall tile at", tile_x, tile_y)
                    else:
                        ch = grid[tile_y][tile_x]
                        print("Printing tile at", tile_x, tile_y)

                    for m in monster_list:
                        if m.x == tile_x and m.y == tile_y:
                            ch = m.char
                            break

                    if dx == 0 and dy == 0:
                        ch = '@'

                    max_y, max_x = dungeon_win.getmaxyx()  # Get window size
                    if 0 <= dy + playerone.indoorsight < max_y and 0 <= dx + playerone.indoorsight < max_x:
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
        # combat_win.refresh()
        # ascii_3d_win.refresh()
        # dbascii_3d_win.refresh()
        stdscr.refresh()  # Refresh main screen **last**

        # Handle movement

        # key = stdscr.getch()
        new_x, new_y = player_x, player_y

        # Handle movement and directional updates

        current_time = time.time()
        if current_time - last_player_update >= player_interval-.45:
            key = handle_input(stdscr)
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
            if 0 <= new_x < grid_width and 0 <= new_y < grid_height and grid[new_y][new_x] == levelmap.tiles["floor"]:
                player_x, player_y = new_x, new_y
            last_player_update = current_time  # Reset timer




        # **Game Over Check**
        if playerone.health <= 0:
            combat_log.append("Game Over - You have died!")
            statuslogs.display_combat_log(combat_win, combat_log)
            combat_win.refresh()  # Refresh combat log one last time
            stdscr.getch()  # Pause before quitting
            break

def rungame():
    # running = False
    # while not running:
    #    try:
    curses.wrapper(main)
    #        running = True
    #    except curses.error:
    #        error_handling.pc_failure()
    #        input("")
