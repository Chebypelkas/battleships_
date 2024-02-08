import pygame as pg
from cells import Cell
from ship import Ship
from random import choice
from constants import CELL_MAP


'''
создаётся игровое поле 10х10, на котором создаются корабли класса Ship и клетки класса Cell
'''


class Board:
    def __init__(self, x_pos, color):
        self.cells = {}
        self.free_cells = []
        self.ships = []
        self.ships_points = []
        letters = 'абвгдеозик'
        for x in range(10):
            for y in range(10):
                key = f'{letters[x] + str(y + 1)}'
                self.cells[key] = Cell(x, y, x_pos, color)
                self.free_cells.append((x, y))
        self.generate_ships()

    def update(self):
        pass

    def draw(self, window: pg.Surface):
        for ship in self.ships:
            ship.draw(window)
        for cell in self.cells.values():
            cell.draw(window)

    # создаёт корабли
    def generate_ships(self):
        self.generate_ship_place(4)
        for _ in range(2):
            self.generate_ship_place(3)
        for _ in range(3):
            self.generate_ship_place(2)
        for _ in range(4):
            self.generate_ship_place(1)

    # выбирает рандомно место для корабля нужного размера
    def generate_ship_place(self, size: int):
        point = choice(self.free_cells)
        bad_points = []
        dir_ = [0, 1, 2, 3]
        while dir_:
            direction = choice(dir_)
            #print(f'\n\nразмер корабля: {size} \nориентация: {direction} \nпозиция: {point} \nсвободные клетки: {self.free_cells} \nплохие клетки: {bad_points} \nточи где стоят корабли: {self.ships_points}')
            match direction:
                # вверх
                case 0:
                    if point[1] - (size - 1) >= 0 and self.is_free('top', size, point):
                        self.generate_ship('top', point, size)
                        break
                    else:
                        dir_.remove(0)
                # вниз
                case 1:
                    if point[1] + (size - 1) <= 9 and self.is_free('bottom', size, point):
                        self.generate_ship('bottom', point, size)
                        break
                    else:
                        dir_.remove(1)
                # право
                case 2:
                    if point[0] + (size - 1) <= 9 and self.is_free('right', size, point):
                        self.generate_ship('right', point, size)
                        break
                    else:
                        dir_.remove(2)
                # лево
                case 3:
                    if point[0] - (size - 1) >= 0 and self.is_free('left', size, point):
                        self.generate_ship('left', point, size)
                        break
                    else:
                        dir_.remove(3)
            if not dir_:
                bad_points.append(point)
                while True:
                    try:
                        point = choice(list(set(self.free_cells).difference(bad_points)))
                        if point not in bad_points:
                            dir_ = [0, 1, 2, 3]
                            break
                    except IndexError:
                        break

    # проверяет можно ли поставить корабль
    def is_free(self, direction: str, size: int, point: tuple) -> bool:
        if direction == 'right':
            for i in range(size + 2):
                for j in range(3):
                    if not_on_board(point[0] + i - 1, point[1] + j - 1):
                        continue
                    if (point[0] + i - 1, point[1] + j - 1) in self.ships_points:
                        return False
            return True
        elif direction == 'left':
            for i in range(size + 2):
                for j in range(3):
                    if not_on_board(point[0] - i + 1, point[1] + j - 1):
                        continue
                    if (point[0] - i + 1, point[1] + j - 1) in self.ships_points:
                        return False
            return True
        elif direction == 'top':
            for i in range(3):
                for j in range(size + 2):
                    if not_on_board(point[0] + i - 1, point[1] - j + 1):
                        continue
                    if (point[0] + i - 1, point[1] - j + 1) in self.ships_points:
                        return False
            return True
        elif direction == 'bottom':
            for i in range(3):
                for j in range(size + 2):
                    if not_on_board(point[0] + i - 1, point[1] + j - 1):
                        continue
                    if (point[0] + i - 1, point[1] + j - 1) in self.ships_points:
                        return False
            return True

    # создаёт корабль
    def generate_ship(self, direction: str, point: tuple, size: int):
        self.ships.append(Ship(self.generate_point_list(direction, point, size)))
        if direction == 'right':
            self.ships_points.extend([(point[0] + i, point[1]) for i in range(size)])
        elif direction == 'left':
            self.ships_points.extend([(point[0] - i, point[1]) for i in range(size)])
        elif direction == 'top':
            self.ships_points.extend([(point[0], point[1] - i) for i in range(size)])
        elif direction == 'bottom':
            self.ships_points.extend([(point[0], point[1] + i) for i in range(size)])
        self.remove_free_cells(point, direction, size)

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
                    if (point[0] + i - 1, point[1] + j - 1) in self.free_cells:
                        self.free_cells.remove((point[0] + i - 1, point[1] + j - 1))
        elif direction == 'left':
            for i in range(size + 2):
                for j in range(3):
                    if (point[0] - i + 1, point[1] + j - 1) in self.free_cells:
                        self.free_cells.remove((point[0] - i + 1, point[1] + j - 1))
        elif direction == 'top':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i - 1, point[1] - j + 1) in self.free_cells:
                        self.free_cells.remove((point[0] + i - 1, point[1] - j + 1))
        elif direction == 'bottom':
            for i in range(3):
                for j in range(size + 2):
                    if (point[0] + i - 1, point[1] + j - 1) in self.free_cells:
                        self.free_cells.remove((point[0] + i - 1, point[1] + j - 1))


class EnemyBoard(Board):
    def __init__(self, x_pos, color):
        super().__init__(x_pos, color)

    def draw(self, window: pg.Surface):
        for cell in self.cells.values():
            cell.draw(window)


def not_on_board(x, y):
    return x < 0 or x > 9 or y < 0 or y > 9