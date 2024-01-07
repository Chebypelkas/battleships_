import pygame as pg
from cells import Cell
from ship import Ship
from random import randint, choice
from constants import CELL_MAP


class Board:
    def __init__(self):
        self.cells = {}
        self.free_cells = []
        self.ships = []
        # сделать чтоб на экране было поле 10x10, клетку можно достать по a1, a2 и т.д.
        letters = 'абвгдежзик'
        for x in range(10):
            for y in range(10):
                key = f'{letters[x] + str(y + 1)}'
                self.cells[key] = Cell(x, y)
                self.free_cells.append((x, y))
        self.generate_ships()

    def update(self):
        pass

    def draw(self, window: pg.Surface):
        for ship in self.ships:
            ship.draw(window)
        for cell in self.cells.values():
            cell.draw(window)

    def generate_ships(self):
        self.generate_ship(4)
        for _ in range(2):
            self.generate_ship(3)
        for _ in range(3):
            self.generate_ship(2)
        for _ in range(4):
            self.generate_ship(1)

    def generate_ship(self, size):
        point = choice(self.free_cells)
        bad_points = []
        dir_ = [0, 1, 2, 3]
        while dir_:
            direction = choice(dir_)

            match direction:
                # вверх
                case 0:
                    if point[1] - (size - 1) >= 0 and self.is_free('top', size, point):
                        self.generate_deck('top', point, size)
                        break
                    else:
                        dir_.remove(0)
                # вниз
                case 1:
                    if point[1] + (size - 1) <= 9 and self.is_free('bottom', size, point):
                        self.generate_deck('bottom', point, size)
                        break
                    else:
                        dir_.remove(1)
                # право
                case 2:
                    if point[0] + (size - 1) <= 9 and self.is_free('right', size, point):
                        self.generate_deck('right', point, size)
                        break
                    else:
                        dir_.remove(2)
                # лево
                case 3:
                    if point[0] - (size - 1) >= 0 and self.is_free('left', size, point):
                        self.generate_deck('left', point, size)
                        break
                    else:
                        dir_.remove(3)
            if not dir_:
                bad_points.append(point)
                while True:
                    point = choice(self.free_cells)
                    if point not in bad_points or set(self.free_cells).issubset(bad_points):
                        break
                dir_ = [0, 1, 2, 3]

    def is_free(self, direction: str, size: int, point: tuple):
        if direction == 'right':
            for i in range(size + 2):
                for j in range(3):
                    if (point[0] + i, point[1] + j) not in self.free_cells:
                        return False
            return True
        elif direction == 'left':
            for i in range(size + 2):
                for j in range(3):
                    if (point[0] - i, point[1] + j) not in self.free_cells:
                        return False
            return True
        elif direction == 'top':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i, point[1] - j) not in self.free_cells:
                        return False
            return True
        elif direction == 'bottom':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i, point[1] + j) not in self.free_cells:
                        return False
            return True

    def generate_deck(self, direction: str, point: tuple, size: int):
        self.ships.append(Ship(self.generate_point_list(direction, point, size)))
        if direction == 'left':
            self.remove_free_cells((point[0] + 1, point[1] - 1), direction, size)
        elif direction == 'right':
            self.remove_free_cells((point[0] - 1, point[1] - 1), direction, size)
        elif direction == 'top':
            self.remove_free_cells((point[0] - 1, point[1] + 1), direction, size)
        elif direction == 'bottom':
            self.remove_free_cells((point[0] - 1, point[1] - 1), direction, size)

    def generate_point_list(self, direction: str, point: tuple, size: int) -> list:
        if direction == 'right':
            return [self.cells[CELL_MAP[point[0] + i, point[1]]] for i in range(size)]
        elif direction == 'left':
            return [self.cells[CELL_MAP[point[0] - i, point[1]]] for i in range(size)]
        elif direction == 'top':
            return [self.cells[CELL_MAP[point[0], point[1] - i]] for i in range(size)]
        elif direction == 'bottom':
            return [self.cells[CELL_MAP[point[0], point[1] + i]] for i in range(size)]

    def remove_free_cells(self, point: tuple, direction: str, size: int):
        if direction == 'right':
            for i in range(size + 2):
                for j in range(3):
                    if (point[0] + i, point[1] + j) in self.free_cells:
                        self.free_cells.remove((point[0] + i, point[1] + j))
        elif direction == 'left':
            for i in range(size + 2):
                for j in range(3):
                    if (point[0] - i, point[1] + j) in self.free_cells:
                        self.free_cells.remove((point[0] - i, point[1] + j))
        elif direction == 'top':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i, point[1] - j) in self.free_cells:
                        self.free_cells.remove((point[0] + i, point[1] - j))
        elif direction == 'bottom':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i, point[1] + j) in self.free_cells:
                        self.free_cells.remove((point[0] + i, point[1] + j))
