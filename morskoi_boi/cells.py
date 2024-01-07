import pygame as pg
from constants import *


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x * WIDTH_WINDOW/10, self.y * HEIGHT_WINDOW/10, WIDTH_WINDOW/10, HEIGHT_WINDOW/10)
        self.is_ship = False

    def update(self):
        pass

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, 'blue', self.rect, 5)
