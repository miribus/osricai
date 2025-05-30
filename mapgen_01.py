#! /usr/bin/env python
# coding: utf-8

# generator-1.py, a simple python dungeon generator by
# James Spencer <jamessp [at] gmail.com>.

# To the extent possible under law, the person who associated CC0 with
# pathfinder.py has waived all copyright and related or neighboring rights
# to pathfinder.py.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import print_function
import random


class Generator():
    def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5,
                 max_room_xy=10, rooms_overlap=False, random_connections=1,
                 random_spurs=3, style="indoor"):

        if style == "indoor":
            CHARACTER_TILES = {'stone': '#',
                               'floor': '.',
                               'wall': '#'}
            self.width = width
            self.height = height
            self.max_rooms = max_rooms
            self.min_room_xy = min_room_xy
            self.max_room_xy = max_room_xy
            self.rooms_overlap = rooms_overlap
            self.random_connections = random_connections
            self.random_spurs = random_spurs
            self.tiles = CHARACTER_TILES
            self.level = []
            self.room_list = []
            self.corridor_list = []
            self.tiles_level = []
            self.style = style


    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0

        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))

        return [x, y, w, h]

    def room_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:

            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.

            if (x < (current_room[0] + current_room[2]) and
                current_room[0] < (x + w) and
                y < (current_room[1] + current_room[3]) and
                current_room[1] < (y + h)):

                return True

        return False


    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type == 'either' and set([0, 1]).intersection(
                 set([x1, x2, y1, y2])):

                join = 'bottom'
            elif (join_type == 'either' and
                  set([self.width - 1, self.width - 2]).intersection(set([x1, x2]))
                  or set([self.height - 1, self.height - 2]).intersection(set([y1, y2]))):

                join = 'top'
            elif join_type == 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join == 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join == 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])

        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # no overlap
        else:
            join = None
            if join_type == 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join == 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join == 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_level(self):
        # Build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []

        max_iters = self.max_rooms * 5

        for a in range(max_iters):
            tmp_room = self.gen_room()

            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]

                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)

            if len(self.room_list) >= self.max_rooms:
                break

        # Connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # Do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # Do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(
                2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # Fill the map
        # Paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # Paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'

            if len(corridor) == 3:
                x3, y3 = corridor[2]

                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'

        # Paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'

                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'

                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'

                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'

                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'

                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'

                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'

                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'

        # Ensure wall thickness
        for _ in range(4):  # Repeat to ensure proper thickness
            new_level = [row[:] for row in self.level]
            for row in range(1, self.height - 1):  # Skip the top and bottom edges
                for col in range(1, self.width - 1):  # Skip the left and right edges
                    if self.level[row][col] == 'wall':
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                new_row, new_col = row + dy, col + dx
                                if 1 <= new_row < self.height - 1 and 1 <= new_col < self.width - 1:  # Skip edges
                                    if self.level[new_row][new_col] == 'stone':
                                        new_level[new_row][new_col] = 'wall'
            self.level = new_level

    def gen_tiles_level(self):

        for row_num, row in enumerate(self.level):
            tmp_tiles = []

            for col_num, col in enumerate(row):
                if col == 'stone':
                    tmp_tiles.append(self.tiles['stone'])
                if col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])
                if col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])

            self.tiles_level.append(''.join(tmp_tiles))

        print('Room List: ', self.room_list)
        print('\nCorridor List: ', self.corridor_list)

        [print(row) for row in self.tiles_level]


    def generate_dungeon_map(self, room_list, corridor_list):
        """
        Generates a 2D grid representing the dungeon.
        Walls are '#' and floors are ' '. Computes an offset so that
        the grid indices start at 0.
        """
        # Determine the boundaries of the dungeon.
        min_x = float('inf')
        min_y = float('inf')
        max_x = 0
        max_y = 0

        for room in room_list:
            x, y, w, h = room
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + w - 1)
            max_y = max(max_y, y + h - 1)

        for corridor in corridor_list:
            for (cx, cy) in corridor:
                min_x = min(min_x, cx)
                min_y = min(min_y, cy)
                max_x = max(max_x, cx)
                max_y = max(max_y, cy)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Create a grid filled with walls.
        grid = [[self.tiles["wall"] for _ in range(width)] for _ in range(height)]

        # Carve out each room.
        for room in room_list:
            rx, ry, rw, rh = room
            offset_x = rx - min_x
            offset_y = ry - min_y
            for j in range(rh):
                for i in range(rw):
                    grid[offset_y + j][offset_x + i] = self.tiles["floor"]

        # Carve out corridors.
        for corridor in corridor_list:
            for i in range(len(corridor) - 1):
                (x1, y1) = corridor[i]
                (x2, y2) = corridor[i+1]
                # Horizontal corridor.
                if y1 == y2:
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        grid[y1 - min_y][x - min_x] = self.tiles["floor"]
                # Vertical corridor.
                elif x1 == x2:
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        grid[y - min_y][x1 - min_x] = self.tiles["floor"]
                else:
                    # If diagonal corridors occur, additional logic would be needed.
                    pass

        return grid, min_x, min_y


if __name__ == '__main__':
    gen = Generator()
    gen.gen_level()
    gen.gen_tiles_level()
    input("press any key to quit")