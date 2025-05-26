import curses

def display_player(stdscr, player):
    """Display player attributes in a sidebar on the right."""
    height, width = stdscr.getmaxyx()  # Get screen size
    stats_x = width - 20  # Reserve last 20 columns for stats
    idx=0
    stdscr.addstr(idx, stats_x, f"Player: {player.name}, {player.type}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"HP: {player.health}, Lvl: {player.level}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"STR: {player.strength}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"DEX: {player.dexterity}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"CON: {player.constitution}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"INT: {player.intelligence}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"WIS: {player.wisdom}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"CHA: {player.charisma}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"----------------------")
    idx += 1
    stdscr.addstr(idx, stats_x, f"Melee HB: {player.m_hitbase}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"Ranged HB: {player.r_hitbase}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"Attack: {player.melee_attack}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"Sight: Indoor: {player.indoorsight}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"    -: Outdoor: {player.outdoorsight}")
    idx += 1
    stdscr.addstr(idx, stats_x, f"Range Dis: {player.range}")
    idx += 1
    for i in range(0, player.level+1):
        if i in player.abilities:
            for a in player.abilities[i]:
                stdscr.addstr(idx, stats_x, f"Abil: {a}")
                idx += 1


def display_combat_log(combat_win, log_messages):
    """Render combat messages in a separate window."""
    combat_win.clear()
    combat_win.box()  # Draws a border around the combat log window

    # Adjust scrolling to always keep last entries visible
    max_lines = 8  # Only display 4 visible lines inside the box
    start_line = max(0, len(log_messages) - max_lines)  # Prevent negative indexing

    for i, msg in enumerate(log_messages[start_line:start_line + max_lines]):
        combat_win.addstr(i + 1, 2, msg[:combat_win.getmaxyx()[1]-4])  # Limit message width

    combat_win.refresh()
