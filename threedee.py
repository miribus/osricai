def render_ascii_3d_view(ascii_3d_win, grid, player_x, player_y, view_distance=5):
    """Render dungeon structure in ASCII 3D form."""

    #ascii_3d_win.clear()
    dungeon_view = extract_dungeon_view(grid, player_x, player_y, view_distance)  # Get real room layout

    for depth, row in enumerate(dungeon_view):
        line = ""

        # Scale width based on distance (perspective effect)
        wall_left = max(0, (ascii_3d_win.getmaxyx()[1] // 2) - depth)
        wall_right = min(ascii_3d_win.getmaxyx()[1], (ascii_3d_win.getmaxyx()[1] // 2) + depth)

        for x, tile in enumerate(row):
            if wall_left <= x <= wall_right:
                line += "█" if tile == "#" else "▒"  # Walls vs open space
            else:
                line += " "

        if 0 <= depth < ascii_3d_win.getmaxyx()[0]:
            ascii_3d_win.addstr(depth, 0, line[:ascii_3d_win.getmaxyx()[1] - 1])

    #ascii_3d_win.refresh()

def extract_dungeon_view(grid, player_x, player_y, radius=5):
    """Get a localized slice of the dungeon grid around the player."""
    view_data = []

    for depth in range(radius, 0, -1):  # From farthest visible tile to closest
        row = ""
        for dx in range(-depth, depth + 1):
            tile_x = player_x + dx
            tile_y = player_y + depth  # Looking forward

            if 0 <= tile_x < len(grid[0]) and 0 <= tile_y < len(grid):
                row += grid[tile_y][tile_x]
            else:
                row += " "  # Out-of-bounds areas

        view_data.append(row)

    return view_data