# monsters.py
import pathfinding
import random


class Monster:
    def __init__(self, x, y, char='M'):
        """
        x, y: Global coordinates (same as defined by your room list).
        char: The character representation of the monster.
        """
        self.x = x
        self.y = y
        self.char = char


def move_toward_player(monsters, dijkstra_map, grid):
    """
    Moves each monster toward the player using the Dijkstra map.

    Args:
        monsters: List of Monster instances.
        dijkstra_map: Precomputed Dijkstra map.
        grid: The dungeon map.
    """
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right

    for monster in monsters:
        best_x, best_y = monster.x, monster.y
        best_cost = dijkstra_map[monster.y][monster.x]

        # Check neighboring tiles for lowest cost
        for dx, dy in directions:
            nx, ny = monster.x + dx, monster.y + dy
            if grid[ny][nx] == '.' and dijkstra_map[ny][nx] < best_cost:
                best_x, best_y = nx, ny
                best_cost = dijkstra_map[ny][nx]

        # Move the monster to the best tile found
        monster.x, monster.y = best_x, best_y

def place_monsters(room_list, num_monsters):
    """
    Choose random positions within rooms to spawn monsters.

    Args:
        room_list: A list of rooms, where each room is defined as [x, y, width, height].
        num_monsters: Total number of monsters to populate.

    Returns:
        A list of Monster instances.
    """
    monsters = []
    for _ in range(num_monsters):
        # Randomly pick a room from the room list.
        room = random.choice(room_list)
        rx, ry, rw, rh = room
        # Pick a random position within the chosen room.
        monster_x = rx + random.randint(0, rw - 1)
        monster_y = ry + random.randint(0, rh - 1)
        monsters.append(Monster(monster_x, monster_y))
    return monsters


def move_toward_player(monsters, dijkstra_map, grid, player_x, player_y):
    """
    Moves each monster toward the player using the Dijkstra map—but only if the monster can see the player.

    Args:
        monsters: List of Monster instances.
        dijkstra_map: Precomputed Dijkstra map.
        grid: The dungeon map.
        player_x, player_y: Player's position.
    """
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right

    for monster in monsters:
        # Check if the monster has line-of-sight to the player
        if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y):
            # If visible, move toward the lowest-cost tile using the Dijkstra map
            best_x, best_y = monster.x, monster.y
            best_cost = dijkstra_map[monster.y][monster.x]

            for dx, dy in directions:
                nx, ny = monster.x + dx, monster.y + dy

                # Ensure nx and ny are within the bounds of the grid
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):

                    if grid[ny][nx] == '.' and dijkstra_map[ny][nx] < best_cost:
                        best_x, best_y = nx, ny
                        best_cost = dijkstra_map[ny][nx]

            # Move the monster to the best tile found
            monster.x, monster.y = best_x, best_y
