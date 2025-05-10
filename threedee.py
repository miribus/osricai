def render_ascii_3d_view(ascii_3d_win, grid, player_x, player_y, player_facing, view_distance=5):
    """Render a refined ASCII 3D dungeon view with correct perspective alignment."""

    #ascii_3d_win.clear()
    max_width = ascii_3d_win.getmaxyx()[1] - 1  # Prevent boundary overflow
    dungeon_view = extract_dungeon_view(grid, player_x, player_y, player_facing, view_distance)  # Get rotated slice

    for depth, row in enumerate(dungeon_view):
        line = ""

        # **NEW Scaling Approach**
        scale_factor = max(4, int((max_width / 3) / (depth + 1)))  # Gradual width reduction
        center_x = max_width // 2  # Center positioning

        for x, tile in enumerate(row):
            left_edge = center_x - scale_factor
            right_edge = center_x + scale_factor

            if left_edge <= x <= right_edge:
                if tile == "#":
                    line += "█"  # Walls
                elif tile == ".":
                    line += "▒"  # Floor shading
                else:
                    line += " "  # Empty space
            else:
                line += " "  # Background fading out

        if 0 <= depth < ascii_3d_win.getmaxyx()[0]:
            ascii_3d_win.addstr(depth, 0, line[:min(len(line), max_width)])

    #ascii_3d_win.refresh()


def render_ascii_3d_view_old(ascii_3d_win, grid, player_x, player_y, player_facing, view_distance=5):
    """Render a refined ASCII 3D dungeon view with correct perspective alignment."""

    #ascii_3d_win.clear()
    max_width = ascii_3d_win.getmaxyx()[1] - 1  # Prevent boundary overflow
    dungeon_view = extract_dungeon_view(grid, player_x, player_y, player_facing, view_distance)  # Get rotated slice

    for depth, row in enumerate(dungeon_view):
        line = ""

        # **NEW Scaling Approach**
        scale_factor = max(4, int((max_width / 2) / (depth + 1)))  # Ensures gradual width reduction
        center_x = max_width // 2  # Center positioning

        for x, tile in enumerate(row):
            left_edge = center_x - scale_factor
            right_edge = center_x + scale_factor

            if left_edge <= x <= right_edge:
                if tile == "#":
                    line += "█"  # Walls
                elif tile == ".":
                    line += "▒"  # Floor shading
                else:
                    line += " "  # Empty space
            else:
                line += " "  # Background fading out

        if 0 <= depth < ascii_3d_win.getmaxyx()[0]:
            ascii_3d_win.addstr(depth, 0, line[:min(len(line), max_width)])

    #ascii_3d_win.refresh()


def render_ascii_3d_debug(ascii_3d_win, grid, player_x, player_y, player_facing, view_distance=5):
    """Render a debug overlay showing the actual dungeon layout in the 3D view."""

    #ascii_3d_win.clear()
    max_width = ascii_3d_win.getmaxyx()[1] - 1  # Prevent boundary overflow
    dungeon_view = extract_dungeon_view(grid, player_x, player_y, player_facing, view_distance)  # Get rotated slice

    for depth, row in enumerate(dungeon_view):
        debug_info = f"{depth}: {row}"  # Prints raw 2D grid row for comparison
        ascii_3d_win.addstr(depth, 0, debug_info[:max_width])  # Ensure it fits within bounds

    #ascii_3d_win.refresh()


def extract_dungeon_view(grid, player_x, player_y, player_facing, radius=5):
    """Extract a slice of the dungeon map oriented based on the player's facing direction."""
    view_data = []

    for depth in range(radius, 0, -1):  # From farthest visible tile to closest
        row = ""
        for dx in range(-depth, depth + 1):  # Adjust horizontal range dynamically
            # Determine tile coordinates based on facing direction
            if player_facing == "north":
                tile_x, tile_y = player_x + dx, player_y - depth
            elif player_facing == "south":
                tile_x, tile_y = player_x + dx, player_y + depth
            elif player_facing == "west":
                tile_x, tile_y = player_x - depth, player_y + dx
            elif player_facing == "east":
                tile_x, tile_y = player_x + depth, player_y + dx

            if 0 <= tile_x < len(grid[0]) and 0 <= tile_y < len(grid):
                row += grid[tile_y][tile_x]  # Extract actual map data
            else:
                row += " "  # Out-of-bounds space

        view_data.append(row)

    return view_data