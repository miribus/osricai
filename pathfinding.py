from collections import deque


def generate_dijkstra_map(grid, player_x, player_y):
    """
    Computes a Dijkstra map where each tile contains the cost (distance) from the player.

    Args:
        grid: The dungeon map (list of lists).
        player_x, player_y: Player's current position.

    Returns:
        A 2D list containing distance values for each tile.
    """
    width = len(grid[0])
    height = len(grid)

    # Initialize map with high values
    dijkstra_map = [[float('inf')] * width for _ in range(height)]
    dijkstra_map[player_y][player_x] = 0  # Player's position starts at 0

    # Breadth-first search queue (starting from player)
    queue = deque([(player_x, player_y)])

    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]

    while queue:
        x, y = queue.popleft()
        current_cost = dijkstra_map[y][x]

        # Check neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == '.':  # Floor tiles only
                if dijkstra_map[ny][nx] > current_cost + 1:
                    dijkstra_map[ny][nx] = current_cost + 1
                    queue.append((nx, ny))

    return dijkstra_map


def has_line_of_sight(grid, x1, y1, x2, y2):
    """
    Determines if there is a clear line-of-sight between two points using Bresenham's line algorithm.

    Args:
        grid: 2D dungeon map.
        x1, y1: Starting coordinates (monster position).
        x2, y2: Target coordinates (player position).

    Returns:
        True if there is a clear LoS, False otherwise.
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        if grid[y1][x1] == '#':  # Check if current tile is a wall
            return False

        # If moving diagonally, ensure both adjacent tiles are passable
        if abs(dx) == abs(dy):  # Diagonal step
            if (0 <= x1 - sx < len(grid[0]) and 0 <= y1 - sy < len(grid)) and \
                    grid[y1][x1 - sx] == '#' and grid[y1 - sy][x1] == '#':  # Check corner blocking
                return False

        # Reached the target (player)
        if x1 == x2 and y1 == y2:
            return True

        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
