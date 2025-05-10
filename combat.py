import random

import pathfinding

def check_and_resolve_combat(monsters, grid, player_x, player_y, player, combat_log, gen):
    """Allows the player to proactively attack monsters before they attack."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles
    chance = 0 # initialize random modifier to hits


    dijkstra_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y)

    for monster in monsters:  # Loop through monsters safely
        if gen.style == "indoor":
            if player.indoorsight > player.range:
                player_attack_range = player.indoorsight  # Define player’s shooting range
            else:
                player_attack_range = player.range
            monster_attack_range = monster.indoorsight
        else: # elif gen.style == "outdoor":
            if player.outdoorsight > player.range:
                player_attack_range = player.outdoorsight  # Define player’s shooting range
            else:
                player_attack_range = player.range
            monster_attack_range = monster.outoorsight
        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y):
            distance = abs(monster.x - player_x) + abs(monster.y - player_y)

            # Player attacks ranged monsters within range
            if monster.behavior == "ranged" and distance <= player_attack_range:
                if player_attack_range > player.indoorsight \
                        or player_attack_range > player.outdoorsight:

                    chance = -50
                roll = random.randrange(1,101)
                hit = False
                if roll in (1, player.r_hitbase-chance):
                    hit = True
                if hit:
                    combat_log.append(f"You fire at {monster.name}! (-{player.attack} HP)")
                    if monster.take_damage(player.attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                else:
                    combat_log.append(f"You fire at {monster.name}! You MISS!)")
                if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and \
                            dijkstra_map[monster.y][monster.x] <= monster_attack_range:
                    combat_log.append(monster.movement_description)
                    combat_log.append(f"{monster.name} shoots at you! (-{monster.attack} HP)")
                    player.take_damage(monster.attack)

            # Player can attack melee monsters **before they strike**
            elif monster.behavior == "melee" and distance == 1:  # Adjacent
                roll = random.randrange(1, 101)
                hit = False
                if roll in (1, player.m_hitbase):
                    combat_log.append(f"You strike first at {monster.name}! (-{player.attack} HP)")
                    if monster.take_damage(player.attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and dijkstra_map[monster.y][monster.x] <= monster_attack_range:
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
