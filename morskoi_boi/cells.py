import pygame as pg
from constants import *


class Cell:
    def __init__(self, x, y, x_pos, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pg.Rect(self.x * WIDTH_WINDOW/20 + x_pos, self.y * HEIGHT_WINDOW/10, WIDTH_WINDOW/20, HEIGHT_WINDOW/10)
        self.is_ship = False

    def update(self):
        pass

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, self.color, self.rect, 5)
