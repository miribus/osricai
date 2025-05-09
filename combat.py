import pathfinding

def check_and_resolve_combat(monsters, grid, player_x, player_y, player, combat_log):
    """Allows the player to proactively attack monsters before they attack."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles

    player_attack_range = 5  # Define player’s shooting range
    monster_attack_range = 5
    dijkstra_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y)

    for monster in monsters:  # Loop through monsters safely
        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y):
            distance = abs(monster.x - player_x) + abs(monster.y - player_y)

            # Player attacks ranged monsters within range
            if monster.behavior == "ranged" and distance <= player_attack_range:
                combat_log.append(f"You fire at {monster.name}! (-{player.attack} HP)")
                if monster.take_damage(player.attack):
                    combat_log.append(f"{monster.name} is slain!")
                    monsters.remove(monster)
                elif pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and \
                            dijkstra_map[monster.y][monster.x] <= monster.line_of_sight:
                    combat_log.append(monster.movement_description)
                    combat_log.append(f"{monster.name} shoots at you! (-{monster.attack} HP)")
                    player.take_damage(monster.attack)

            # Player can attack melee monsters **before they strike**
            elif monster.behavior == "melee" and distance == 1:  # Adjacent
                combat_log.append(f"You strike first at {monster.name}! (-{player.attack} HP)")
                if monster.take_damage(player.attack):
                    combat_log.append(f"{monster.name} is slain!")
                    monsters.remove(monster)
                elif pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and dijkstra_map[monster.y][monster.x] <= 10:
                    # Move toward the player, but stop adjacent
                    best_x, best_y = monster.x, monster.y
                    best_cost = dijkstra_map[monster.y][monster.x]

                    for dx, dy in directions:
                        nx, ny = monster.x + dx, monster.y + dy
                        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == '.' and dijkstra_map[ny][nx] < best_cost:
                            best_x, best_y = nx, ny
                            best_cost = dijkstra_map[ny][nx]

                    # Prevent monster from occupying player's tile
                    if (best_x, best_y) != (player_x, player_y):
                        monster.x, monster.y = best_x, best_y
                        combat_log.append(monster.movement_description)
