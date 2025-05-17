import random
import pathfinding

def check_and_resolve_combat(monsters, grid, player_x, player_y, player, combat_log, gen):
    """Allows the player to proactively attack monsters before they attack."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles
    chance = 0  # Initialize random modifier to hits

    dijkstra_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y)

    for monster in monsters:  # Loop through monsters safely
        if gen.style == "indoor":
            player_attack_range = max(player.indoorsight, player.range)
            monster_attack_range = monster.indoorsight
        else:  # Outdoor
            player_attack_range = max(player.outdoorsight, player.range)
            monster_attack_range = monster.outdoorsight

        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y):
            distance = max(abs(monster.x - player_x), abs(monster.y - player_y))

            # Player ranged attack
            if ("ranged_attack" in player.abilities.get(player.level, []) or
                "magic_attack" in player.abilities.get(player.level, [])) and distance <= player_attack_range:
                if player_attack_range > player.indoorsight or player_attack_range > player.outdoorsight:
                    chance = -50

                roll = random.randrange(1, 101)
                if roll in range(1, player.r_hitbase + chance):
                    combat_log.append(f"You fire at {monster.name}! (-{player.melee_attack} HP)")
                    if monster.take_damage(player.melee_attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                else:
                    combat_log.append(f"You fire at {monster.name}! You MISS!)")

            # Player melee attack
            elif ("melee_attack" in player.abilities.get(player.level, []) or
                  "magic_attack" in player.abilities.get(player.level, [])) and distance <= 1:
                roll = random.randrange(1, 101)
                if roll in range(1, player.m_hitbase):
                    combat_log.append(f"You strike first at {monster.name}! (-{player.melee_attack} HP)")
                    if monster.take_damage(player.melee_attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                else:
                    combat_log.append(f"You swing at {monster.name}! You MISS!)")

            # Monster attack
            if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and \
                    dijkstra_map[monster.y][monster.x] <= monster_attack_range:
                combat_log.append(f"{monster.name} attacks you! (-{monster.melee_attack} HP)")
                player.take_damage(monster.melee_attack)
