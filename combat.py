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
                    movement_description = monster.movement_description.split("\n")
                    for m in movement_description:
                        combat_log.append(m)
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
                else:
                    combat_log.append(f"You swing at {monster.name}! You MISS!)")
