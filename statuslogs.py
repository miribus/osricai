import curses

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


def display_combat_log(combat_win, log_messages):
    """Render combat messages in a separate window."""
    combat_win.clear()
    combat_win.box()  # Draws a border around the combat log window

    # Adjust scrolling to always keep last entries visible
    max_lines = 4  # Only display 4 visible lines inside the box
    start_line = max(0, len(log_messages) - max_lines)  # Prevent negative indexing

    for i, msg in enumerate(log_messages[start_line:start_line + max_lines]):
        combat_win.addstr(i + 1, 2, msg[:combat_win.getmaxyx()[1]-4])  # Limit message width

    combat_win.refresh()