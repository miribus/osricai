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


def display_player(stdscr, player):
    """Display player attributes in a sidebar on the right."""
    height, width = stdscr.getmaxyx()  # Get screen size
    stats_x = width - 20  # Reserve last 20 columns for stats

    stdscr.addstr(0, stats_x, f"Player: {player.name}")
    stdscr.addstr(1, stats_x, f"HP: {player.health}")
    stdscr.addstr(2, stats_x, f"STR: {player.strength}")
    stdscr.addstr(3, stats_x, f"DEX: {player.dexterity}")
    stdscr.addstr(4, stats_x, f"CON: {player.constitution}")
    stdscr.addstr(5, stats_x, f"INT: {player.intelligence}")
    stdscr.addstr(6, stats_x, f"WIS: {player.wisdom}")
    stdscr.addstr(7, stats_x, f"CHA: {player.charisma}")

def main(stdscr):
    playerone = player.Player("MyName")
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(False)
    stdscr.keypad(True)

    grid, offset_x, offset_y = generate_dungeon_map(room_list, corridor_list)
    grid_height, grid_width = len(grid), len(grid[0])

    radius = 5  # Viewport size
    first_room = room_list[0]
    player_x = first_room[0] + first_room[2] // 2 - offset_x
    player_y = first_room[1] + first_room[3] // 2 - offset_y

    num_monsters = 5
    monster_list = monsters.place_monsters(room_list, num_monsters)
    for m in monster_list:
        m.x -= offset_x
        m.y -= offset_y

    while True:
        stdscr.clear()
        dij_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y)
        monsters.move_toward_player(monster_list, dij_map, grid, player_x, player_y)

        # Draw dungeon viewport centered on player
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                tile_x, tile_y = player_x + dx, player_y + dy
                distance = (dx**2 + dy**2) ** 0.5

                if distance > radius:
                    ch = ' '  # Outside visible range
                elif tile_x < 0 or tile_x >= grid_width or tile_y < 0 or tile_y >= grid_height:
                    ch = '#'  # Walls if out of bounds
                else:
                    ch = grid[tile_y][tile_x]

                for m in monster_list:
                    if m.x == tile_x and m.y == tile_y:
                        ch = m.char
                        break

                if dx == 0 and dy == 0:
                    ch = '@'

                stdscr.addch(dy + radius, dx + radius, ch)

        # Draw player stats in the sidebar
        display_player(stdscr, playerone)

        stdscr.refresh()

        # Handle movement
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

        if 0 <= new_x < grid_width and 0 <= new_y < grid_height and grid[new_y][new_x] == '.':
            player_x, player_y = new_x, new_y
curses.wrapper(main)
