# monsters.py
import time
import pathfinding
import random
import json
import os
import error_handling

occupied_positions = set()  # Track used positions
monchars = []

class Monster:
    def __init__(self, x, y, name, hp, attack, hitbase, damage, indoorsight, outdoorsight, movement_description, behavior, char='M', attackrate=1):
        """
        Monster attributes:
        - x, y: Position
        - name: Name of the monster
        - hp: Health points
        - attack: Damage dealt per attack
        - movement_description: Description of monster movement
        - behavior: 'melee' or 'ranged'
        - char: Character representation
        """
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.attack = attack
        self.hitbase = hitbase
        self.damage = damage
        self.indoorsight = indoorsight
        self.outdoorsight = outdoorsight
        self.movement_description = movement_description
        self.behavior = behavior
        self.char = char  # Default 'M' for monsters
        monchars.append(self.char)
        self.attackrate = attackrate
        self.last_attack_time = int(time.time())  # Track last attack time

    def take_damage(self, damage):
        """Reduce monster's HP and check if defeated."""
        print(f"MONSTER DAMAGE TAKEN! {damage}")
        self.hp -= damage
        if self.hp <= 0:
            return True  # Monster is defeated
        return False


def load_monsters_from_json(grid, file_path=os.path.join(os.getcwd(), "rogue_monsters","monsters.json"), name="all", monster_list=False, levelmap=None):
    """Load monster data from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)

    if not monster_list:
        global occupied_positions
        monster_list = []
        for monster in data["monsters"]:
            if name in monster["name"] or name == "all":
                spawn_count = random.randint(monster["spawn_min"], monster["spawn_max"])
                # Create a Monster object (adjust attributes based on your class structure)
                if spawn_count:
                    for _ in range(spawn_count):
                        x, y, occupied_positions = find_random_position(grid, levelmap)
                        if "melee_attack" in monster:
                            new_monster = Monster(
                                x=x,
                                y=y,
                                name=monster["name"],
                                hp=monster["hp"],
                                attack=monster["melee_attack"],
                                hitbase=monster["m_hitbase"],
                                damage=monster["damage"],
                                indoorsight=monster["indoorsight"],
                                outdoorsight=monster["outdoorsight"],
                                movement_description=monster["movement_description"],
                                behavior=monster["behavior"],
                                char=monster["icon"],
                                attackrate=monster["attackrate"]
                            )
                        elif "ranged_attack" in monster:
                            new_monster = Monster(
                                x=x,
                                y=y,
                                name=monster["name"],
                                hp=monster["hp"],
                                attack=monster["ranged_attack"],
                                hitbase=monster["r_hitbase"],
                                damage=monster["damage"],
                                indoorsight=monster["indoorsight"],
                                outdoorsight=monster["outdoorsight"],
                                movement_description=monster["movement_description"],
                                behavior=monster["behavior"],
                                char=monster["icon"],
                                attackrate = monster["attackrate"]
                            )
                        elif "magic_attack" in monster:
                            new_monster = Monster(
                                x=x,
                                y=y,
                                name=monster["name"],
                                hp=monster["hp"],
                                attack=monster["magic_attack"],
                                damage=monster["damage"],
                                indoorsight=monster["indoorsight"],
                                outdoorsight=monster["outdoorsight"],
                                movement_description=monster["movement_description"],
                                behavior=monster["behavior"],
                                char=monster["icon"],
                                attackrate = monster["attackrate"]
                            )
                        monster_list.append(new_monster)

    print(monster_list, "ML")
    return monster_list


def find_random_position(grid, levelmap):
    global occupied_positions
    """Find a random, unoccupied position in the grid."""
    max_x = len(grid[0])  # Width of grid
    max_y = len(grid)  # Height of grid

    while True:
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        if grid[y][x] == levelmap.tiles["floor"] and (x, y) not in occupied_positions:
            occupied_positions.add((x, y))
            return x, y, occupied_positions


def place_monsters(grid, room_list, monster_data):
    """Places monsters in valid locations using safety checks."""
    placed_monsters = []

    for monster in monster_data:
        # x, y = find_safe_position(grid, room_list, occupied_positions)
        # x, y = find_random_position(grid, room_list, occupied_positions)
        # monster.x = x  # Update position here
        # monster.y = y
        print(f"Placing: {monster.name} at {monster.x} and {monster.y}")
        placed_monsters.append(monster)

    return placed_monsters

def move_toward_player(monsters, dijkstra_map, grid, player_x, player_y, combat_log, levelmap):
    global occupied_positions
    """Moves monsters toward the player using Dijkstra map logic."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles
    dijkstra_map = dijkstra_map

    for monster in monsters:
        placed = False
        retry = 5
        while not placed and retry > 0:
            if levelmap.style == "indoor":
                monster_attack_range = monster.indoorsight
            else: # elif gen.style == "outdoor":
                monster_attack_range = monster.outdoorsight
            print("monster", monster.name, monster.indoorsight, monster_attack_range, player_x, player_y)

            if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y, levelmap, [monster.char for monster in monsters]) and dijkstra_map[monster.y][
                monster.x] <= monster_attack_range:
                print("movecheck", monster.name)
                # Move toward the player, but stop adjacent
                best_x, best_y = monster.x, monster.y
                print("movecheck", best_x, best_y, 'xy')
                best_cost = dijkstra_map[monster.y][monster.x]

                for dx, dy in directions:
                    nx, ny = monster.x + dx, monster.y + dy
                    if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == levelmap.tiles["floor"] and dijkstra_map[ny][
                        nx] < best_cost:
                        best_x, best_y = nx, ny
                        best_cost = dijkstra_map[ny][nx]

                # Prevent monster from occupying player's tile
                if (best_x, best_y) != (player_x, player_y):
                    # Ensure the position isn't already occupied
                    if (best_x, best_y) in occupied_positions:
                        alt_x, alt_y = find_alternate_position(monster, player_x, player_y, occupied_positions)
                        if (alt_x, alt_y) != (best_x, best_y):  # Ensure a new position was found
                            best_x, best_y = alt_x, alt_y

                    # Move the monster
                    monster.x, monster.y = best_x, best_y
                    occupied_positions.add((best_x, best_y))  # Update occupied positions
                    movement_description = monster.movement_description.split("\n")
                    for m in movement_description:
                        combat_log.append(m)
                    placed = True
            print("retry", retry)
            retry -= 1


def find_alternate_position(monster, player_x, player_y, occupied_positions):
    """Find the next best open position near the player."""
    possible_moves = [
        (monster.x + 1, monster.y),
        (monster.x - 1, monster.y),
        (monster.x, monster.y + 1),
        (monster.x, monster.y - 1),
        (monster.x + 1, monster.y + 1),
        (monster.x - 1, monster.y - 1)
    ]

    # Filter out occupied positions
    valid_moves = [pos for pos in possible_moves if pos not in occupied_positions]

    if valid_moves:
        # Prioritize positions that move the monster toward the player
        valid_moves.sort(key=lambda pos: abs(pos[0] - player_x) + abs(pos[1] - player_y))

        return valid_moves[0]  # Choose the closest valid move to the player

    return monster.x, monster.y  # Default to staying put