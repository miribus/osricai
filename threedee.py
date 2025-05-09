def render_ascii_3d_view(ascii_3d_win, grid, player_x, player_y, view_distance=10):
    """Render a basic faux ASCII 3D perspective based on the dungeon layout."""
    ascii_3d_win.clear()

    max_width = ascii_3d_win.getmaxyx()[1] - 1  # Ensure within bounds

    # Loop through depth layers (from close to far)
    for depth in range(view_distance, 0, -1):
        line = ""

        # Simulate walls getting narrower as they extend
        wall_left = max(0, (ascii_3d_win.getmaxyx()[1] // 2) - depth)
        wall_right = min(ascii_3d_win.getmaxyx()[1], (ascii_3d_win.getmaxyx()[1] // 2) + depth)

        for x in range(ascii_3d_win.getmaxyx()[1]):
            if wall_left <= x <= wall_right:
                line += "█"  # Wall closer
            else:
                line += "▒"  # Background shading

        # Only write inside valid rows AFTER building the `line`
        if 0 <= view_distance - depth < ascii_3d_win.getmaxyx()[0]:
            ascii_3d_win.addstr(view_distance - depth, 0, line[:min(len(line), max_width)])

    ascii_3d_win.refresh()