# monsters.py
import pathfinding
import random
import json
import os

class Monster:
    def __init__(self, x, y, name, hp, attack, damage, movement_description, behavior, char='M'):
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
        self.damage = damage
        self.movement_description = movement_description
        self.behavior = behavior
        self.char = char  # Default 'M' for monsters

    def take_damage(self, damage):
        """Reduce monster's HP and check if defeated."""
        self.hp -= damage
        if self.hp <= 0:
            return True  # Monster is defeated
        return False

def find_safe_position(grid, room_list, occupied_positions):
    """Finds a valid empty tile to spawn a monster."""
    while True:
        room = random.choice(room_list)  # Pick a random room
        x = room[0] + random.randint(1, room[2] - 2)
        y = room[1] + random.randint(1, room[3] - 2)

        # Ensure tile is open and not occupied
        if grid[y][x] == '.' and (x, y) not in occupied_positions:
            occupied_positions.add((x, y))  # Mark as taken
            return x, y

def load_monsters_from_json(file_path=os.path.join(os.getcwd(), "rogue_monsters","monsters.json")):
    """Load monster data from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)

    monster_list = []
    for monster in data["monsters"]:
        # Create a Monster object (adjust attributes based on your class structure)
        new_monster = Monster(
            x=0,  # This will be set later
            y=0,
            name=monster["name"],
            hp=monster["hp"],
            attack=monster["attack"],
            damage=monster["damage"],
            movement_description=monster["movement_description"],
            behavior=monster["behavior"],
            char=monster["icon"]
        )

        monster_list.append(new_monster)

    return monster_list

def place_monsters(grid, room_list, monster_data):
    """Places monsters in valid locations using safety checks."""
    placed_monsters = []
    occupied_positions = set()  # Track taken spots

    for monster in monster_data:
        x, y = find_safe_position(grid, room_list, occupied_positions)
        monster.x = x  # Update position here
        monster.y = y
        placed_monsters.append(monster)

    return placed_monsters



def move_toward_player(monsters, dijkstra_map, grid, player_x, player_y, player, combat_log):
    """Moves monsters toward the player using Dijkstra map logic."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles

    for monster in monsters:
        if monster.behavior == "melee":
            if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y) and dijkstra_map[monster.y][monster.x] <= 10:
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
